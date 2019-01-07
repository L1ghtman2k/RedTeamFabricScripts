def change_root_password(connect):
    connect.sudo("sh -c 'echo \"changeme\nchangeme\" | passwd admin'")


# Only PfSense:
def secure_level(connect):
    connect.run("sysctl kern.securelevel=3")
    connect.run("echo 'sysctl kern.securelevel=3' > /usr/local/etc/rc.d/script.sh")
    connect.run("chmod +x /usr/local/etc/rc.d/script.sh")


def allow_root_ssh(connect):
    connect.sudo("sed -i '/PermitRootLogin/c\PermitRootLogin yes' /etc/ssh/sshd_config")
    connect.sudo("service ssh restart")