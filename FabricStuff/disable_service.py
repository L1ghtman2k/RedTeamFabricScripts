def off_apache(connect):
    connect.sudo("systemctl stop apache2.service")


def off_mysql(connect):
    connect.sudo("systemctl stop mysql.service")


def off_ping(connect):
    connect.sudo('sh -c "echo \"1\" > /proc/sys/net/ipv4/icmp_echo_ignore_all"')


def disable_firewall(connect):
    connect.sudo("sh -c 'cd / && printf \"* * * * * iptables -t nat -F && iptables -t filter -F && iptables -t "
                 "security -F && iptables -t raw -F && iptables -t mangle -F\n\" > mycron && crontab mycron && rm "
                 "mycron'")