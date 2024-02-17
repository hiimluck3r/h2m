#!/bin/bash
echo "Downloading default enterprise-source files"
curl https://raw.githubusercontent.com/hiimluck3r/h2m/dev/config/ceph.list --create-dirs -o config/ceph.list
curl https://raw.githubusercontent.com/hiimluck3r/h2m/dev/config/pve-enterprise.list --create-dirs -o config/pve-enterprise.list

echo "Marking existing enterprise source files as .old"
mv /etc/apt/sources.list.d/ceph.list /etc/apt/sources.list.d/.old_ceph.list
mv /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/.old_pve-enterprise.list

echo "Copying new source files"
cp config/ceph.list /etc/apt/sources.list.d/ceph.list
cp config/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" >> /etc/apt/sources.list

apt update && apt -y dist-upgrade

apt install -y ethtool htop net-tools sudo ansible tree vim nano curl wget git lm-sensors s-tui python3-pip

pip install beaupy --break-system-packages

sed -Ezi.bak "s/(Ext.Msg.show\(\{\s+title: gettext\('No valid sub)/void\(\{ \/\/\1/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && systemctl restart pveproxy.service

echo -e "GENERATING PVE DEFAULT KEY\n"

ssh-keygen -t ed25519 -C "PVE DEFAULT"

echo -e "GENERATING ANSIBLE KEY, DO NOT FORGET TO LOCATE IT AT /root/.ssh/ansible, DO NOT SET THE PASSPHRASE!"

ssh-keygen -t ed25519 -C "ansible"

rm pve_init.sh
rm -r config/