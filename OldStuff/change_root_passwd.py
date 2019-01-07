from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"sysadmin@10.{i}."
	hosts.extend([single+"1.10", single+"1.20", single+"2.2", single+"2.3"])

for hostelele in hosts:
	try:
		config = Config(overrides={'sudo':{'password':'changeme'}})
		c = Connection(hostelele, connect_kwargs={"password":"changeme"}, config=config)
		c.sudo("sh -c 'echo \"changeme\nchangeme\" | passwd admin'")
		msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
		print(msg.format(c))

	except:
		continue
