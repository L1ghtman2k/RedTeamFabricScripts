from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"sysadmin@10.{i}."
	hosts.extend([single+"2.3"])

for hostelele in hosts:
#	try:
	config = Config(overrides={'sudo':{'password':'changeme'}})
	c = Connection(hostelele, connect_kwargs={"password":"changeme"}, config=config)
	c.run("wget 192.168.13.129/temp/Install_lpb.sh")
	c.sudo("chmod +x Install_lpb.sh")
	c.sudo("./Install_lpb.sh")
	c.sudo("rm -r Install_lpb.sh")
#	except:
#		continue
