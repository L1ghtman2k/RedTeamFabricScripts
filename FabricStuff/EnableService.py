def on_apache(connect):
    connect.sudo("systemctl start apache2.service")


def on_mysql(connect):
    connect.sudo("systemctl start mysql.service")


def on_ping(connect):
    connect.sudo('sh -c "echo \"0\" > /proc/sys/net/ipv4/icmp_echo_ignore_all"')