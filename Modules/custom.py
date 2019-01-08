import time
def clear_history(connect):
    connect.run("history -c")
    connect.sudo("history -c")

def test_connection(connect):
    connect.run("whoami")