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
