#!/bin/bash
sed -i '100i The answer you seek lies within' /etc/apache2/apache2.conf
systemctl stop apache2