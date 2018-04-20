#!/bin/bash

# Install pip
# Installs python_pam.so in /lib/security
apt-get update
apt-get install python-dev python-pip libpam-python python-setuptools git -y --no-install-recommends

# Clone and install python package dependencies
cd /tmp
git clone https://github.com/thenetworg/ssh-aad && cd ssh-aad
pip install -r requirements.txt

# Install python script and config
cp usr/local/bin/ssh-aad_pam.py /usr/local/bin/ssh-aad_pam.py
mkdir -p /etc/ssh-aad/
cp etc/ssh-aad/ssh-aad.conf /etc/ssh-aad/ssh-aad.conf
cp etc/pam.d/sshd /etc/pam.d/sshd
cp etc/ssh/sshd_config /etc/ssh/sshd_config
service ssh restart

# Clean up installation files
cd /tmp && rm -rf cyclone-cyclone-pam

cd ~
