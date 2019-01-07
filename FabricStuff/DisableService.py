def off_apache(connect):
    connect.sudo("systemctl stop apache2.service")


def off_mysql(connect):
    connect.sudo("systemctl stop mysql.service")


def off_ping(connect):
    connect.sudo('sh -c "echo \"1\" > /proc/sys/net/ipv4/icmp_echo_ignore_all"')