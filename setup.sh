#!/bin/bash
echo "Installing dependencies: Ansible"

apt -y install ansible
python3 installer.py

./services.sh

ansible-playbook -i inventory --ask-vault-pass --ask-become-pass playbooks/setup.yml