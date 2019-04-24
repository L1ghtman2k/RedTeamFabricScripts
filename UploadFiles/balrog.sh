#!/bin/bash
systemctl stop apache2
while true
do
sleep 60s
systemctl stop apache2
done