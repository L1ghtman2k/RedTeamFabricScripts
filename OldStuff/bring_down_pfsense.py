from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"root@10.{i}."
	hosts.extend([single+"1.1"])

for hostelele in hosts:
	try:
		c = Connection(hostelele, connect_kwargs={"password":"changeme"})
		c.run("poweroff")
	except:
		continue
