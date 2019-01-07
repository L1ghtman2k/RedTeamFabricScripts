from fabric import Connection, Config
import getpass
hosts = []
for i in range (7,12):
	single=f"root@10.{i}."
	hosts.extend([single+"2.2"])

for hostelele in hosts:
	try:
		config = Config(overrides={'sudo':{'password':'changeme'}})
		c = Connection(hostelele, connect_kwargs={"password":"VerySecure"} , config=config)
		c.sudo("systemctl stop apache2.service")
	except:
		continue
