from fabric import Connection, Config
import types
import re
from termcolor import colored
import colorama
import argparse
import invoke
import sys
import multiprocessing
from Modules import *


def imports():
    methods = {}
    p = re.compile("^__[a-zA-Z0-9_.-]*__$")
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and "Modules." in val.__name__:
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
    colorama.init()
    try:
        fn(connect)
        print(colored(f"{ip} executed successfully", "green"))
    except invoke.exceptions.UnexpectedExit as e:
        fail=open("fail.txt", "a")
        fail.write(f"{ip}\n")
        fail.close()
        print(colored(f"Command Failed On {ip}", "red"))
        print(e)
    except:
        fail=open("fail.txt", "a")
        fail.write(f"{ip}\n")
        fail.close()
        print(colored(f"Command Failed On {ip} for unknown reason", "red"))
        e = sys.exc_info()[0]
        print(e)



def name_to_module(name, namespace):
    for module in namespace:
        if f"Modules.{name}" == module.__name__:
            return module
    return None


def helper():
    output = "Available modules and functions\n"
    for module, methods in imports().items():
        for method in methods:
            output += f"{module.__name__.replace('Modules.', '')} : {method}\n"
    return output


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        print(helper())
        sys.exit(2)


class Formatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


if __name__ == '__main__':
    parser = MyParser(description=f"Specify the function, module, and the file containing IP addresses.\n{helper()}\n"
    f"example usage: python prebake secure_level --password Change.me! --timeout 60 --file output.txt\n\n"
    "Hint: Use IPgenerator to generate ip addresses", formatter_class=Formatter)
    parser.add_argument("module", help="Module from which the function should be imported")
    parser.add_argument("function", help="Function name that you would like to use")
    parser.add_argument("--password", help="Password to connect to a remote host", default="changeme")
    parser.add_argument("--timeout", help="Timeout for the connection", default=None, type=int)
    parser.add_argument("--file", help="File containing comma separated values of ip addresses", default="output.txt")
    args = parser.parse_args()
    available_functions = imports()
    module = name_to_module(args.module, available_functions.keys())

    ip_list=[]

    if args.function in available_functions[module]:
        for txt_file in args.file.split(","):
            with open(txt_file, "r") as file:
                ip_list.extend(file.read().split('\n'))

        fail=open("fail.txt", "w")
        fail.close()
        for ip in ip_list:
            if ip:
                p = multiprocessing.Process(target=wrapper, args=(getattr(module, args.function), ip,
                                                                  args.password, args.timeout))
                p.start()
    else:
        print("Wrong Module or Function")
        helper()
