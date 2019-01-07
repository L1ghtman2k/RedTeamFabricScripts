def parrot_party(connect):
    connect.sudo("DISPLAY=:0 gnome-terminal -e \"/bin/bash -l -c \'curl parrot.live; cat -\'\"")
