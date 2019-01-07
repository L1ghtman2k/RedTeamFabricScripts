from fabric import Connection, Config
import invoke
import time
import multiprocessing

hosts = ["aibek@192.168.1.62", "aibek@192.168.1.73"]


def wrapper(fn, ip, password):
	config = Config(overrides={'sudo': {'password': password}})
	connect = Connection(ip, connect_kwargs={"password": password}, config=config)
	try:
		fn(connect)
		print(f"{ip} executed successfully")
	except invoke.exceptions.UnexpectedExit:
		print(f"Command Failed On {ip}")


def whoami(connect):
	connect.sudo("git clone https://github.com/fail2ban/fail2ban.git")


if __name__ =='__main__':
	p1 = multiprocessing.Process(target=wrapper, args=(whoami, "aibek@192.168.1.62", "changeme"))
	p1.start()
	p2 = multiprocessing.Process(target=wrapper, args=(whoami, "aibek@192.168.1.73", "changeme"))
	p2.start()




