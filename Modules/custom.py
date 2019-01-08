def clear_history(connect):
    connect.run("history -c")
    connect.sudo("history -c")
