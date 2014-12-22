#!/usr/bin/env python3

from os import walk
from os.path import join
from xattr import xattr

"""
Helper Functions
"""
def walk_action(root_dir, action):
    for root, dirs, files in walk(root_dir):
        for file_name in files:
            full_file_name = join(root, file_name)
            yield action(full_file_name)

generate_sha512 = lambda f: gen_file_hash(f, hashlib.sha512)
add_sha512 = lambda f: add_hash_if_necessary(f, hashlib.sha512)
check_sha512 = lambda f: check_hash(f, hashlib.sha512)
print_sha512 = lambda f: print_hash(f, hashlib.sha512)

def gen_file_hash(f, hashlib_func):
    fh = open(f, 'rb')
    file_hash = hashlib_func()
    data = fh.read(1024**2)
    while (len(data) > 0):
        file_hash.update(data)
        data = fh.read(1024**2)
    fh.close()
    return f, file_hash.hexdigest(), file_hash.name

def add_hash_if_necessary(f, hashlib_func):
    try:
        _x = xattr(file_name)
        _h = hashlib_func()
        attribute_name = 'user.%s' % _h.name
        if not attribute_name in _x.list():
            _fh, _ = gen_file_hash(f, hashlib_func)
            return f, add_hash(f, attribute_name, _fh)
    except:
        return False

def add_hash(file_name, hash_label, hash_value):
    try:
        _x = xattr(file_name)
        _x.set(_b(hash_label), _b(hash_value))
        return True
    except:
        # Setting hash xattr failed
        return False

def _b(input_string):
    return bytes(input_string, 'utf-8')

def check_hash(file_name, hashlib_func):
    # TODO
    return None

def print_hash(file_name, hashlib_func):
    # TODO
    return None
