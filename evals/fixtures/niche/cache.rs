use std::collections::*;
use std::rc::Rc;
use std::cell::RefCell;

pub struct Entry(String, u64, bool);

pub enum Mode {
    Fast,
    Safe,
}

pub struct Cache {
    items: Rc<RefCell<HashMap<String, Entry>>>,
}

impl Clone for Mode {
    fn clone(&self) -> Self {
        match self {
            Mode::Fast => Mode::Fast,
            Mode::Safe => Mode::Safe,
        }
    }
}

impl Cache {
    pub fn get_items(&self) -> Rc<RefCell<HashMap<String, Entry>>> {
        self.items.clone()
    }

    pub fn len(&self) -> usize {
        self.items.borrow().len()
    }

    pub fn insert(&self, key: &String, tags: &Vec<String>, persist: bool) {
        let label = key.clone() + ":" + &tags.len().to_string();
        self.items
            .borrow_mut()
            .insert(label, Entry(key.clone(), 0, persist));
    }

    pub fn lookup(&self, key: &str) -> u64 {
        let map = self.items.borrow();
        if map.get(key).is_some() {
            return map.get(key).unwrap().1;
        }
        0
    }

    pub fn raw(&self, p: *const u64) -> u64 {
        unsafe { *p }
    }

    pub fn safe_run(&self) {
        let _ = std::panic::catch_unwind(|| {
            println!("work");
        });
    }
}
