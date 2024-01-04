#!/bin/bash

sed -i 's|deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise|# deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise|g' /etc/apt/sources.list.d/pve-enterprise.list 

sed -i 's|https://enterprise.proxmox.com/debian/ceph-quincy|# https://enterprise.proxmox.com/debian/ceph-quincy|g' /etc/apt/source.list.d/ceph.list

echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" >> /etc/apt/sources.list

apt update && apt -y dist-upgrade

apt install -y ethtool htop net-tools sudo tree vim nano curl wget git lm-sensors s-tui

sed -Ezi.bkp "s/(Ext.Msg.show
\(\{\s+title: gettext\('No valid sub)/void\(\{ \/\/\1/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && systemctl restart pveproxy.service

echo -e "GENERATING PVE DEFAULT KEY\n"

ssh-keygen -t ed25519 -C "PVE DEFAULT"

echo -e "GENERATING ANSIBLE KEY, DO NOT FORGET TO LOCATE IT AT /root/.ssh/ansible, DO NOT SET THE PASSPHRASE!"

ssh-keygen -t ed25519 -C "ansible"
