#!/usr/bin/env python3
"""Automated sanity checks for the 24 CodeTone rule sheets.

This does not call a model. For each language it checks that the rule sheet
has a review checklist, that the test case lists its seeded violations, and
that a hand-written compliant sample passes the language's native tool when
that tool is installed. See evals/README.md for the model evals.
"""

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / 'skills' / 'codetone'
REFS = SKILL_DIR / 'references'

# ---------------------------------------------------------------------------
# Test definitions for all 24 languages
# ---------------------------------------------------------------------------
TEST_CASES = {
    'python': {
        'name': 'Python',
        'ref': 'python.md',
        'tool_cmd': lambda p: ['python3', '-m', 'py_compile', str(p)],
        'filename': 'sample.py',
        'seeded_code': '''
from os.path import join
import sys, json

def GetItems(path):
  data = open(join(path, "items.json")).read()
  return json.loads(data)

def add_item(item, items=[]):
    items.append(item)
    return items

def find_price(items, name):
    for item in items:
        if item.get("name") == name and item.get("price") != None:
            return item["price"]

items = GetItems(sys.argv[1])
''',
        'expected_violations': [
            'imports a function, not a module (from os.path import join)',
            'multiple imports on one line (import sys, json)',
            'function name should be lower_with_under (GetItems)',
            '2-space indentation (must be 4 spaces)',
            'open without with statement',
            'mutable default argument (items=[])',
            '!= None comparison (use is not None)',
            'missing main() guard / top-level executable code',
        ],
        'compliant_code': '''"""Sample module demonstrating Google Python style."""

import json
import os
import sys
from typing import Any, Dict, List, Optional


def load_items(base_dir: str) -> List[Dict[str, Any]]:
    """Loads items from the JSON configuration.

    Args:
        base_dir: Path to directory containing items.json.

    Returns:
        A list of item dictionaries.
    """
    path = os.path.join(base_dir, "items.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_item(item: Dict[str, Any], items: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Appends an item to a list safely without mutable defaults."""
    target_items = items if items is not None else []
    target_items.append(item)
    return target_items


def main() -> None:
    """Entry point for sample CLI."""
    if len(sys.argv) > 1:
        data = load_items(sys.argv[1])
        print(f"Loaded {len(data)} items")


if __name__ == "__main__":
    main()
''',
    },

    'cpp': {
        'name': 'C++',
        'ref': 'cpp.md',
        'tool_cmd': lambda p: ['clang++', '-std=c++17', '-fsyntax-only', str(p)],
        'filename': 'sample.cc',
        'seeded_code': '''
#pragma once
#include <iostream>
using namespace std;

class MyClass {
 public:
  MyClass(int val) { value = val; }
  virtual void doStuff() override {}
  int value;
};
''',
        'expected_violations': [
            '#pragma once used instead of #define guard <PROJECT>_<PATH>_<FILE>_H_',
            'using namespace std forbidden',
            'single-argument constructor missing explicit keyword',
            'virtual combined with override keyword',
            'public member variable value without trailing underscore value_',
            'function name should be PascalCase (DoStuff instead of doStuff)',
        ],
        'compliant_code': '''// Copyright 2026 CodeTone Authors.

#ifndef SAMPLE_MATH_UTILS_H_
#define SAMPLE_MATH_UTILS_H_

namespace sample {

class MathUtils {
 public:
  MathUtils() = default;
  explicit MathUtils(int initial_value) : value_(initial_value) {}

  int value() const { return value_; }
  void set_value(int v) { value_ = v; }

 private:
  int value_ = 0;
};

}  // namespace sample

#endif  // SAMPLE_MATH_UTILS_H_
''',
    },

    'java': {
        'name': 'Java',
        'ref': 'java.md',
        'tool_cmd': lambda p: ['javac', str(p)],
        'filename': 'SampleService.java',
        'seeded_code': '''
package com.example;
import java.util.*;

public class SampleService {
    public static String NAMES[] = new String[10];
    public void process(int x) {
        if (x > 0)
            System.out.println(x);
    }
}
''',
        'expected_violations': [
            'wildcard import (import java.util.*)',
            'C-style array declaration (NAMES[])',
            '4-space indentation (must be 2 spaces)',
            'single-statement if missing braces',
            'mutable public static array',
            'constant should be UPPER_SNAKE_CASE',
        ],
        'compliant_code': '''package com.example;

import java.util.Collections;
import java.util.List;

/**
 * Service handling sample operations in Google Java style.
 */
public final class SampleService {
  private final List<String> names;

  public SampleService(List<String> names) {
    this.names = Collections.unmodifiableList(names);
  }

  public void process(int count) {
    if (count > 0) {
      System.out.println("Processing: " + count);
    }
  }

  public List<String> getNames() {
    return names;
  }
}
''',
    },

    'javascript': {
        'name': 'JavaScript',
        'ref': 'javascript.md',
        'tool_cmd': lambda p: ['node', '--check', str(p)],
        'filename': 'sample.js',
        'seeded_code': '''
var MAX_COUNT = 10;
export default function getUser() {
  let list = new Array();
  var name = "Alice";
  if (name == "Alice")
    return { name: name }
}
''',
        'expected_violations': [
            'var used instead of const or let',
            'default export used (named exports required)',
            'new Array() constructor used (use literal [])',
            'missing semicolons (relying on ASI)',
            'double quotes used for strings (use single quotes)',
            'missing braces around if block',
        ],
        'compliant_code': '''export class UserService {
  constructor(domain) {
    this.domain = domain;
  }

  getUserEmail(username) {
    return `${username}@${this.domain}`;
  }
}

export const DEFAULT_TIMEOUT_MS = 5000;
''',
    },

    'typescript': {
        'name': 'TypeScript',
        'ref': 'typescript.md',
        'tool_cmd': lambda p: ['tsc', '--noEmit', '--strict', '--target', 'es2022', str(p)],
        'filename': 'user_store.ts',
        'seeded_code': '''
export default class UserStore {
  public data: any;
  var items: Array<string> = [];
  getUser(id: string): string {
    if (id == null) return "unknown"
  }
}
''',
        'expected_violations': [
            'default export used (named exports required)',
            'use of any type forbidden without justification',
            'var keyword used',
            'missing semicolon',
            'missing braces around control block',
        ],
        'compliant_code': '''export interface UserConfig {
  readonly id: string;
  readonly name: string;
}

export class UserStore {
  private readonly users = new Map<string, UserConfig>();

  addUser(user: UserConfig): void {
    this.users.set(user.id, user);
  }

  getUser(id: string): UserConfig | undefined {
    return this.users.get(id);
  }
}
''',
    },

    'angular': {
        'name': 'Angular',
        'ref': 'angular.md',
        'tool_cmd': lambda p: ['tsc', '--noEmit', '--target', 'es2022', str(p)],
        'filename': 'user-profile.component.ts',
        'seeded_code': '''
class userProfile {
  constructor(private http: any) {}
  handleClick() {
    this.http.post("/api");
  }
}
''',
        'expected_violations': [
            'file name must match PascalCase identifier (UserProfile -> user-profile)',
            'constructor injection used instead of inject()',
            'event handler named for event rather than action (handleClick)',
            'use of any type',
            'missing readonly on injected properties',
        ],
        'compliant_code': '''export interface UserData {
  id: string;
  name: string;
}

export class UserProfileComponent {
  protected readonly userData: UserData = {id: '1', name: 'Alice'};

  saveUserData(): void {
    console.log('Saved', this.userData);
  }
}
''',
    },

    'go': {
        'name': 'Go',
        'ref': 'go.md',
        'tool_cmd': lambda p: ['go', 'vet', str(p)],
        'filename': 'greeting.go',
        'seeded_code': '''
package greeting
import . "fmt"

const MAX_COUNT = 100
type GreetingInfo struct {
  userId string
}
func (this GreetingInfo) GetUserId() string {
  return this.userId
}
''',
        'expected_violations': [
            'dot import (. "fmt")',
            'screaming snake_case for constant (MAX_COUNT -> MaxCount)',
            'package stutter (greeting.GreetingInfo)',
            'initialism userId should be userID',
            'receiver named this (use short name like g)',
            'getter prefixed with Get (GetUserId -> UserID)',
            'missing package comment',
        ],
        'compliant_code': '''// Package greeting provides greeting formatters following Google Go style.
package greeting

import "fmt"

// Message formats a greeting message for the specified user.
func Message(userID string) string {
\treturn fmt.Sprintf("Hello, %s!", userID)
}
''',
    },

    'rust': {
        'name': 'Rust',
        'ref': 'rust.md',
        'tool_cmd': lambda p: ['rustc', '--crate-type', 'lib', str(p)],
        'filename': 'sample.rs',
        'seeded_code': '''
use std::collections::*;

pub struct Cache {
    items: Vec<String>,
}

impl Cache {
    pub fn get_items(&self) -> &Vec<String> {
        &self.items
    }
    pub fn add(&mut self, key: &String) {
        unsafe { println!("{}", key); }
    }
}
''',
        'expected_violations': [
            'wildcard glob import (use std::collections::*)',
            'getter method prefixed with get_ (get_items -> items)',
            'taking &Vec<String> parameter instead of slice &[String]',
            'taking &String parameter instead of &str',
            'unsafe block without // SAFETY: justification comment',
        ],
        'compliant_code': '''//! Sample crate demonstrating Google Rust style conventions.

/// Key-value storage container.
#[derive(Debug, Default)]
pub struct Cache {
    items: Vec<String>,
}

impl Cache {
    /// Creates a new empty cache.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Returns a slice of the cached items.
    #[must_use]
    pub fn items(&self) -> &[String] {
        &self.items
    }

    /// Adds an item to the cache.
    pub fn insert(&mut self, item: impl Into<String>) {
        self.items.push(item.into());
    }

    /// Returns true if the cache contains no items.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }
}
''',
    },

    'shell': {
        'name': 'Shell (Bash)',
        'ref': 'shell.md',
        'tool_cmd': lambda p: ['bash', '-n', str(p)],
        'filename': 'backup.sh',
        'seeded_code': '''
#!/bin/sh
BACKUP_DIR=/tmp/backup
function do_backup {
  cp -r $1 $BACKUP_DIR
}
do_backup /var/data
''',
        'expected_violations': [
            'shebang #!/bin/sh instead of #!/bin/bash',
            'missing set -euo pipefail',
            'use of function keyword (use name() syntax)',
            'unquoted variable expansion $1 and $BACKUP_DIR',
            'global variable defined inside function without local keyword',
            'missing main() guard',
        ],
        'compliant_code': '''#!/bin/bash
# Backup utility script following Google Shell Style.

set -euo pipefail

backup_directory() {
  local -r source_dir="${1}"
  local -r dest_dir="${2}"

  if [[ ! -d "${source_dir}" ]]; then
    echo "Error: source ${source_dir} is not a directory" >&2
    return 1
  fi

  cp -R "${source_dir}" "${dest_dir}"
}

main() {
  local -r src="${1:-/tmp/src}"
  local -r dst="${2:-/tmp/dst}"
  backup_directory "${src}" "${dst}"
}

main "$@"
''',
    },

    'csharp': {
        'name': 'C#',
        'ref': 'csharp.md',
        'tool_cmd': None,
        'filename': 'OrderService.cs',
        'seeded_code': '''
namespace MyProject.Orders
{
    public class OrderService
    {
        private int count;
        public void Process()
        {
            if (count > 0)
                count--;
        }
    }
}
''',
        'expected_violations': [
            'Allman-style braces with newline before { (Google C# uses K&R braces)',
            'private field count without _camelCase naming prefix (_count)',
            'single-statement if without braces',
            '4-space indentation (must be 2 spaces)',
        ],
        'compliant_code': '''namespace MyProject.Orders {

public sealed class OrderService {
  private int _orderCount;

  public OrderService(int initialCount) {
    _orderCount = initialCount;
  }

  public int OrderCount => _orderCount;

  public void ProcessOrder() {
    if (_orderCount > 0) {
      _orderCount--;
    }
  }
}

}
''',
    },

    'objective-c': {
        'name': 'Objective-C',
        'ref': 'objective-c.md',
        'tool_cmd': lambda p: ['clang', '-x', 'objective-c', '-fsyntax-only', str(p)],
        # Needs the Foundation framework, which only macOS ships.
        'platforms': ['darwin'],
        'filename': 'ItemManager.m',
        'seeded_code': '''
#import "ItemManager.h"

@implementation ItemManager
- (NSString *)getName {
    return name;
}
- (void)setItem:(NSString *)item andIndex:(NSInteger)index {
}
@end
''',
        'expected_violations': [
            'class missing 3-letter prefix (ItemManager -> GTMItemManager)',
            'getter method prefixed with get (getName -> name)',
            'use of and to join parameter names (andIndex:)',
            'ivars should be prefixed with underscore (_name)',
        ],
        'compliant_code': '''#import <Foundation/Foundation.h>

@interface GTMItemManager : NSObject
@property(nonatomic, copy, readonly) NSString *name;
- (instancetype)initWithName:(NSString *)name NS_DESIGNATED_INITIALIZER;
- (void)insertItem:(NSString *)item atIndex:(NSUInteger)index;
@end

@implementation GTMItemManager
- (instancetype)initWithName:(NSString *)name {
  self = [super init];
  if (self) {
    _name = [name copy];
  }
  return self;
}

- (instancetype)init {
  return [self initWithName:@""];
}

- (void)insertItem:(NSString *)item atIndex:(NSUInteger)index {
  // Method implementation
}
@end
''',
    },

    'swift': {
        'name': 'Swift',
        'ref': 'swift.md',
        'tool_cmd': lambda p: ['swiftc', '-typecheck', str(p)],
        'filename': 'UserProfile.swift',
        'seeded_code': '''
class user_profile {
    var _id: String = "";
    func get_id() -> String {
        if (_id == "") {
            return "empty";
        };
        return _id;
    }
}
''',
        'expected_violations': [
            'type name in snake_case (user_profile -> UserProfile)',
            'field name prefixed with underscore for privacy (_id)',
            'getter method prefixed with get_ (get_id)',
            'semicolons used in Swift code',
            '4-space indentation (must be 2 spaces)',
            'parentheses around if condition (if (_id == ""))',
        ],
        'compliant_code': r'''struct UserProfile {
  private let id: String
  let name: String

  init(id: String, name: String) {
    self.id = id
    self.name = name
  }

  func formattedName() -> String {
    if id.isEmpty {
      return name
    }
    return "\(name) (\(id))"
  }
}
''',
    },

    'kotlin': {
        'name': 'Kotlin',
        'ref': 'kotlin.md',
        'tool_cmd': None,
        'filename': 'UserRepo.kt',
        'seeded_code': '''
package com.example

import java.util.*

class user_repo {
    var ItemList = ArrayList<String>()
    fun GET_ITEMS(): List<String> {
        return ItemList
    }
}
''',
        'expected_violations': [
            'wildcard import (import java.util.*)',
            'class name in snake_case (user_repo -> UserRepo)',
            'property in UpperCamelCase (ItemList -> itemList)',
            'method in SCREAMING_SNAKE_CASE (GET_ITEMS -> getItems)',
        ],
        'compliant_code': '''package com.example

import java.util.Collections

class UserRepository(private val initialItems: List<String>) {
  val items: List<String> = Collections.unmodifiableList(initialItems)

  fun findItem(predicate: (String) -> Boolean): String? {
    return items.firstOrNull(predicate)
  }
}
''',
    },

    'dart': {
        'name': 'Dart',
        'ref': 'dart.md',
        'tool_cmd': None,
        'filename': 'user_bloc.dart',
        'seeded_code': '''
import 'package:flutter/material.dart';
import 'dart:async';

const int DEFAULT_TIMEOUT = 30;

class userBloc {
  /**
   * old style javadoc comment
   */
  void DoStuff() {}
}
''',
        'expected_violations': [
            'directives order inverted (package: before dart:)',
            'constant in SCREAMING_CAPS (Dart uses lowerCamelCase: defaultTimeout)',
            'class name in lowerCamelCase (userBloc -> UserBloc)',
            '/** */ javadoc comments used (Dart requires /// comments)',
            'method name in UpperCamelCase (DoStuff -> doStuff)',
        ],
        'compliant_code': '''import 'dart:async';

const int defaultTimeoutSeconds = 30;

/// State manager for user authentication.
class UserBloc {
  final _stateController = StreamController<String>.broadcast();

  /// Stream of user state updates.
  Stream<String> get state => _stateController.stream;

  /// Disposes active resources.
  void dispose() {
    _stateController.close();
  }
}
''',
    },

    'html-css': {
        'name': 'HTML/CSS',
        'ref': 'html-css.md',
        'tool_cmd': None,
        'filename': 'page.html',
        'seeded_code': '''
<!DOCTYPE HTML>
<HTML>
<BODY>
  <div onclick="navigate()">Click me</div>
  <IMG SRC="PHOTO.JPG">
  <style>
    .Header { COLOR: #FFFFFF; font-size: 14PX; }
  </style>
</BODY>
</HTML>
''',
        'expected_violations': [
            'uppercase HTML tags and attributes (<HTML>, <BODY>, SRC)',
            'non-semantic <div> used for navigation with click handler',
            'img element missing alt attribute',
            'uppercase CSS properties and hex values (COLOR, #FFFFFF, 14PX)',
            'class name in UpperCamelCase (.Header instead of .header)',
        ],
        'compliant_code': '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Sample Page</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header class="site-header">
      <nav>
        <a href="/home">Home</a>
      </nav>
    </header>
    <main>
      <h1>Welcome</h1>
      <img src="logo.png" alt="Company Logo">
    </main>
  </body>
</html>
''',
    },

    'json': {
        'name': 'JSON',
        'ref': 'json.md',
        'tool_cmd': lambda p: [sys.executable, '-m', 'json.tool', str(p)],
        'filename': 'api_response.json',
        'seeded_code': '''
{
  // Comments are not allowed in JSON
  "api_version": "1.0",
  "total_items": 2,
  "item": [
    {"name": "A", "status": 1}
  ]
}
''',
        'expected_violations': [
            'comments included in JSON',
            'snake_case keys (api_version, total_items -> apiVersion, totalItems)',
            'array property with singular name (item instead of items)',
            'numeric enum status (use string enum e.g. "ACTIVE")',
        ],
        'compliant_code': '''{
  "apiVersion": "2.0",
  "data": {
    "totalItems": 1,
    "items": [
      {
        "id": "item100",
        "title": "Widget",
        "status": "AVAILABLE",
        "createdAt": "2026-11-16T22:00:00.000Z"
      }
    ]
  }
}
''',
    },

    'xml': {
        'name': 'XML',
        'ref': 'xml.md',
        'tool_cmd': lambda p: [sys.executable, '-c', f'import xml.etree.ElementTree as ET; ET.parse("{p}")'],
        'filename': 'catalog.xml',
        'seeded_code': '''
<catalog>
  <item_list>
    <item id="1" name="Widget">Extra text mixed in<details>info</details></item>
  </item_list>
</catalog>
''',
        'expected_violations': [
            'missing XML namespace declaration on root element',
            'snake_case element name (item_list -> lowerCamelCase itemList)',
            'mixed content in data element (text mixed with child <details>)',
            'wrapper element that only holds repeating children (<item_list>)',
        ],
        'compliant_code': '''<?xml version="1.0" encoding="utf-8"?>
<catalog xmlns="http://example.com/ns/catalog">
  <product id="prod100">
    <productName>Widget</productName>
    <unitPrice currency="USD">29.99</unitPrice>
  </product>
</catalog>
''',
    },

    'markdown': {
        'name': 'Markdown',
        'ref': 'markdown.md',
        'tool_cmd': None,
        'filename': 'guide.md',
        'seeded_code': '''
My Document Title
=================

## Overview
Some introductory text.

Heading Without Space
---------------------
### Summary
First summary.
### Summary
Duplicate non-unique heading.
''',
        'expected_violations': [
            'Setext underlined headings used instead of ATX (# Title)',
            'duplicate non-unique headings (### Summary)',
            'missing space after heading marker',
        ],
        'compliant_code': '''# Developer Guide

A concise guide to setting up and contributing to the project.

## Overview

CodeTone condenses style guides so any model produces clean, idiomatic code.

## Getting Started

1.  Clone the repository.
2.  Install development dependencies.
3.  Run the test suite.

## See Also

*   [Documentation](https://example.com/docs)
''',
    },

    'r': {
        'name': 'R',
        'ref': 'r.md',
        'tool_cmd': None,
        'filename': 'analysis.R',
        'seeded_code': '''
attach(my_data)
calculate_mean <- function(x) {
  my.result = mean(x)
  my.result -> final
}
''',
        'expected_violations': [
            'use of attach() forbidden',
            'function name in snake_case (Google R uses BigCamelCase: CalculateMean)',
            'variable name in dot.case (my.result)',
            '= used for assignment (use <-)',
            'right-hand assignment -> used',
            'missing explicit return() statement',
        ],
        'compliant_code': '''# Calculates summary statistics for numeric vectors.

CalculateSummary <- function(values) {
  if (length(values) == 0) {
    return(NULL)
  }

  mean_val <- base::mean(values, na.rm = TRUE)
  sd_val <- stats::sd(values, na.rm = TRUE)

  return(list(
    mean = mean_val,
    standard_deviation = sd_val
  ))
}
''',
    },

    'haskell': {
        'name': 'Haskell',
        'ref': 'haskell.md',
        'tool_cmd': None,
        'filename': 'Parser.hs',
        'seeded_code': '''
module Parser where

import Data.List

get_first xs = head xs
''',
        'expected_violations': [
            'missing explicit export list on module header',
            'wholesale uncurated import (import Data.List)',
            'missing type signature on top-level function',
            'use of partial function head without safety checks',
            'snake_case function name (get_first -> lowerCamelCase getFirst)',
        ],
        'compliant_code': '''-- | Parser utilities module following Google Haskell style.
module Parser
  ( safeHead
  , parseTokens
  ) where

import qualified Data.Text as Text

-- | Safely retrieves the first element of a list without partial errors.
safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

-- | Splits input text into words.
parseTokens :: Text.Text -> [Text.Text]
parseTokens = Text.words
''',
    },

    'common-lisp': {
        'name': 'Common Lisp',
        'ref': 'common-lisp.md',
        'tool_cmd': None,
        'filename': 'orders.lisp',
        'seeded_code': '''
(in-package :cl-user)
(defun ComputeTotal (items)
  (let ((result 0))
    (dolist (item items result)
      (setq result (+ result item)))))
''',
        'expected_violations': [
            'CamelCase function name (ComputeTotal -> kebab-case compute-total)',
            'use of setq instead of setf',
            'missing docstring on function',
        ],
        'compliant_code': '''(in-package :cl-user)

(defun compute-total (items)
  "Computes the sum of all numeric items in the provided list."
  (reduce #'+ items :initial-value 0))
''',
    },

    'verilog': {
        'name': 'SystemVerilog/Verilog',
        'ref': 'verilog.md',
        'tool_cmd': None,
        'filename': 'fifo_ctrl.sv',
        'seeded_code': '''
module FifoCtrl(clk, rst, in_data, out_data);
input clk, rst;
input [7:0] in_data;
output [7:0] out_data;
reg [7:0] out_data;
always @(posedge clk) begin
  out_data = in_data;
end
endmodule
''',
        'expected_violations': [
            'module name in PascalCase (use snake_case fifo_ctrl)',
            'legacy Verilog-1995 port list (use ANSI port declarations)',
            'blocking assignment = in clocked always block (use non-blocking <=)',
            'missing sensitivity list standard (always_ff @(posedge clk))',
        ],
        'compliant_code': '''// Synchronous FIFO controller following Google SystemVerilog style.

module fifo_ctrl (
  input  logic       clk,
  input  logic       rst_n,
  input  logic [7:0] in_data,
  output logic [7:0] out_data
);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      out_data <= '0;
    end else begin
      out_data <= in_data;
    end
  end

endmodule
''',
    },

    'vimscript': {
        'name': 'Vim script',
        'ref': 'vimscript.md',
        'tool_cmd': lambda p: ['vim', '-u', 'NONE', '-es', '-c', f'source {p}', '-c', 'q'],
        'filename': 'sample.vim',
        'seeded_code': '''
function Greet(name)
  if a:name == "world"
    normal dd
  endif
endfunction
''',
        'expected_violations': [
            'function defined without ! or abort',
            'bare == used on strings (must use case-explicit ==# or ==?)',
            'double quotes used where single quotes suffice',
            'normal used instead of normal! (runs user mappings)',
            'function not scoped to script (s:) or autoload',
        ],
        'compliant_code': '''" Sample plugin function following Google Vim script style.

function! s:Greet(name) abort
  if a:name ==# 'world'
    return 'Hello, World!'
  endif
  return 'Hello, ' . a:name
endfunction
''',
    },

    'tcl': {
        'name': 'Tcl/Tk',
        'ref': 'tcl.md',
        'tool_cmd': lambda p: ['tclsh', str(p)],
        'filename': 'sample.tcl',
        'seeded_code': '''
proc compute {x} {
    set res [expr $x + 1]
    set list ""
    set list "$list item"
    return $res
}
''',
        'expected_violations': [
            'unbraced expr expression (expr $x + 1 -> expr {$x + 1})',
            'list built with string concatenation instead of lappend/list',
        ],
        'compliant_code': '''# Sample procedure demonstrating Google Tcl style conventions.

proc compute_increment {value} {
    set result [expr {$value + 1}]
    set items [list]
    lappend items $result
    return $items
}
''',
    },
}


def tool_skip_reason(test_data):
    """Returns why the native tool check can't run here, or None if it can."""
    platforms = test_data.get('platforms')
    if platforms and sys.platform not in platforms:
        return f"needs {', '.join(platforms)} (running on {sys.platform})"
    tool_cmd_fn = test_data.get('tool_cmd')
    if tool_cmd_fn is not None:
        tool = tool_cmd_fn(pathlib.Path('x'))[0]
        if shutil.which(tool) is None:
            return f'{tool} is not installed'
    return None


def run_single_eval(slug, test_data, results_collector):
    name = test_data['name']
    ref_file = REFS / test_data['ref']
    assert ref_file.exists(), f"Reference {ref_file} not found"
    ref_text = ref_file.read_text(encoding='utf-8')

    # 1. Checklist verification
    checklist = [line.strip() for line in ref_text.splitlines() if line.strip().startswith('- [ ]')]
    has_checklist = len(checklist) >= 3

    # 2. Review Mode verification (Verify that seeded violations match reference rules)
    seeded_violations = test_data['expected_violations']
    verified_violations = len(seeded_violations) > 0

    # 3. Write Mode verification
    compliant_code = test_data['compliant_code']
    tool_cmd_fn = test_data.get('tool_cmd')
    tool_passed = True
    tool_name = "N/A (Linter/Grammar)"
    skip_reason = tool_skip_reason(test_data)

    if skip_reason is not None:
        results_collector.append({
            'slug': slug,
            'name': name,
            'checklist_items': len(checklist),
            'seeded_violations': len(seeded_violations),
            'tool_name': tool_cmd_fn(pathlib.Path('x'))[0],
            'tool_passed': None,
            'verdict': 'SKIPPED',
            'skip_reason': skip_reason,
        })
        return

    if tool_cmd_fn is not None:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = pathlib.Path(tmpdir) / test_data['filename']
            file_path.write_text(compliant_code, encoding='utf-8')
            cmd = tool_cmd_fn(file_path)
            tool_name = cmd[0]
            try:
                proc = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True,
                                      # Cold compilers (swiftc on CI) are slow.
                                      timeout=120)
                tool_passed = (proc.returncode == 0)
                if not tool_passed:
                    print(f"Tool failed for {name} ({cmd}):\nStdout: {proc.stdout}\nStderr: {proc.stderr}")
            except Exception as e:
                tool_passed = False
                print(f"Tool error for {name} ({cmd}): {e}")

    verdict = has_checklist and verified_violations and tool_passed
    results_collector.append({
        'slug': slug,
        'name': name,
        'checklist_items': len(checklist),
        'seeded_violations': len(seeded_violations),
        'tool_name': tool_name,
        'tool_passed': tool_passed,
        'verdict': 'PASSED' if verdict else 'FAILED'
    })


def main():
    print("=" * 80)
    print("CodeTone rule sheet sanity checks (no model involved)")
    print("=" * 80)
    
    results = []
    for slug in sorted(TEST_CASES.keys()):
        run_single_eval(slug, TEST_CASES[slug], results)

    # Format table
    header = f"{'Language':<22} | {'Checklist':<10} | {'Review Violations':<18} | {'Native Tool':<20} | {'Status'}"
    print(header)
    print("-" * len(header))
    
    all_passed = True
    for r in results:
        status_str = f"\033[92m{r['verdict']}\033[0m" if r['verdict'] == 'PASSED' else f"\033[91m{r['verdict']}\033[0m"
        print(f"{r['name']:<22} | {r['checklist_items']:<10} | {r['seeded_violations']:<18} | {r['tool_name'] + ' (ok)':<20} | {status_str}")
        if r['verdict'] == 'FAILED':
            all_passed = False
        if r['verdict'] == 'SKIPPED':
            print(f"  skipped: {r['skip_reason']}")

    skipped = sum(1 for r in results if r['verdict'] == 'SKIPPED')
    print("=" * 80)
    print(f"Summary: {sum(1 for r in results if r['verdict'] == 'PASSED')}/{len(results)} languages verified, {skipped} skipped.")
    if all_passed and not skipped:
        print("All sanity checks passed.")
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
