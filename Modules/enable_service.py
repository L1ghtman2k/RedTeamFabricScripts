def on_apache(connect):
    connect.sudo("systemctl start apache2.service")


def on_mysql(connect):
    connect.sudo("systemctl start mysql.service")


def on_ping(connect):
    connect.sudo('sh -c "echo \"0\" > /proc/sys/net/ipv4/icmp_echo_ignore_all"')


def tyler_apache_enable_loop(connect):
    connect.run("ps -aux | grep balrog.sh | grep root | awk '{print $2}' > kill_proc")
    try: # this is so bad LOL, but who the hell cares
        connect.sudo("sh -c 'while read in; do sudo kill -9 \"$in\" ; done < kill_proc'")
    except:
        pass
    connect.sudo('rm kill_proc')
    on_apache(connect)
