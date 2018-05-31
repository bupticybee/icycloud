#!/bin/bash
apt-get update
apt-get install -y --no-install-recommends lshell
cp /lshell_build/lshell.conf /etc/
chsh -s /usr/bin/lshell root
chsh -s /usr/bin/lshell icycloud
