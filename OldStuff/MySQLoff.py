from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"sysadmin@10.{i}."
	hosts.extend([single+"2.3"])

for hostelele in hosts:
	try:
		config = Config(overrides={'sudo':{'password':'changeme'}})
		c = Connection(hostelele, connect_kwargs={"password":"changeme"}, config=config)
		c.sudo("systemctl stop mysql.service")
		msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
		print(msg.format(c))

	except:
		continue
