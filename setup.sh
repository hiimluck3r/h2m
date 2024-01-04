#!/bin/bash
source /etc/os-release
echo "Installing dependencies: git, wget, Ansible, Helm, Python, pyyaml"

curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
apt install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
apt update

#todo: check for sources (eternal loop on update && upgrade)

apt -y install git wget python3 ansible helm python3-pip && apt -y dist-upgrade
pip install pyyaml

#sudo pacman -S git wget python ansible helm python-pyyaml

python3 installer.py