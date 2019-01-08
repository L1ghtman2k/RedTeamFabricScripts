def download_gnome(connect):
    connect.sudo("apt-get update -y")
    connect.sudo("apt-get install gnome-terminal curl -y")
