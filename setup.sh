#!/bin/bash
source /etc/os-release
echo "Installing dependencies: git, wget, Ansible, Helm, Python, pyyaml"

if [ "$NAME" = "Ubuntu" ] || [ "$NAME" = "Debian" ]; then
    sudo apt install git wget python ansible helm pip
    sudo pip install pyyaml
else
    sudo pacman -S git wget python ansible helm python-pyyaml
fi

python3 installer.py