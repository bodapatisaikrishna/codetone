#!/usr/bin/env python3
from os.path import join
import logging
import sys, json


def GetItems(path):
  data = open(join(path, "items.json")).read()
  return json.loads(data)


def add_item(item, items=[]):
    items.append(item)
    return items


def summarize(items):
    """summarize items"""
    result = ""
    for i in items:
        result = result + i["name"] + ", "
    if len(items) == 0:
        return None
    return result


def load_or_default(path):
    try:
        return GetItems(path)
    except:
        logging.info(f"could not load {path}")
        return []


def find_price(items, name):
    for item in items:
        if item.get("name") == name and item.get("price") != None and item.get("in_stock") == True:
            return item["price"]


items = load_or_default(sys.argv[1])
print(summarize(items))
