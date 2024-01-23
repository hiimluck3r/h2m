#!/bin/bash
echo "Installing dependencies: Ansible, Helm, pyyaml"

curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
apt install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
apt update

apt -y install ansible helm python-pyyaml && apt -y dist-upgrade

python3 installer.py

./services.sh