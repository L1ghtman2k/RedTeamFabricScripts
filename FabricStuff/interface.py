from FabricStuff.imports import *  # Bad Practice
from fabric import Connection, Config
import types
import re
import argparse
import invoke


def imports():
    methods = {}
    p = re.compile("^__[a-zA-Z0-9_.-]*__$")
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and "FabricStuff" in val.__name__:
            for method in dir(val):
                if not p.match(method):
                    if val in methods:
                        methods[val].append(method)
                    else:
                        methods[val] = [method]
    return methods


def wrapper(fn, ip, password, timeout=None):
    config = Config(overrides={'sudo': {'password': password}})
    connect = Connection(ip, connect_kwargs={"password": password}, config=config, connect_timeout=timeout)
    try:
        fn(connect)
        print(f"{ip} executed successfully")
    except invoke.exceptions.UnexpectedExit as e:
        print(f"Command Failed On {ip}")
        print(e)


if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Specify the function, module, and the file containing IP addresses")
    parser.add_argument("--function", help="Function name that you would like to use", default=None)
    parser.add_argument("--module", help="Module from which the function should be imported", default=None)
    parser.add_argument("--file", help="File containing comma separated values of ip addresses", default="output.txt")
    available_functions = imports()
    args = parser.parse_args()
    for modules, methods in available_functions.items():
        for method in methods:
            print(f"{modules.__name__} : {method}")
