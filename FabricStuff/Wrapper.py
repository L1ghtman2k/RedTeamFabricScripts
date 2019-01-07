from fabric import Connection, Config
import invoke


def wrapper(fn, ip, password):
    config = Config(overrides={'sudo': {'password': password}})
    connect = Connection(ip, connect_kwargs={"password": password}, config=config)
    try:
        fn(connect)
        # connect.run("history -c")
        # connect.sudo("history -c")
        print(f"{ip} executed successfully")
    except invoke.exceptions.UnexpectedExit:
        print(f"Command Failed On {ip}")
