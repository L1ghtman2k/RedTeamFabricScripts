from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"admin@10.{i}."
	hosts.extend([single+"1.10" ,single+"1.20"])

for hostelele in hosts:
	try:
		config = Config(overrides={'sudo':{'password':'changeme'}})
		c = Connection(hostelele, connect_kwargs={"password":"changeme"}, config=config)
		c.sudo("DISPLAY=:0 gnome-terminal -e \"/bin/bash -l -c \'curl parrot.live; cat -\'\"")
	except:
		continue
