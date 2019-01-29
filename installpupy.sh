cd ~
apt-get install git libssl1.0-dev libffi-dev python-dev python-pip tcpdump python-virtualenv -y
git clone --recursive https://github.com/n1nj4sec/pupy
cd pupy
python create-workspace.py -DG pupyw
export PATH=$PATH:~/.local/bin
