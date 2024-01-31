#!/bin/bash
echo "Installing dependencies: Ansible"

apt -y install ansible
python3 installer.py

./services.sh