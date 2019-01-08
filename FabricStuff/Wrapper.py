from fabric import Connection, Config
import invoke


def wrapper(fn, ip, password, timeout=None):
    config = Config(overrides={'sudo': {'password': password}})
    connect = Connection(ip, connect_kwargs={"password": password}, config=config, connect_timeout=timeout)
    try:
        fn(connect)
        print(f"{ip} executed successfully")
    except invoke.exceptions.UnexpectedExit:
        print(f"Command Failed On {ip}")

