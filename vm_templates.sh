#!/bin/bash

# Download Ubuntu minimal image
echo "Downloading an Ubuntu minimal image"
wget -O ubuntu-20.04-minimal.img https://cloud-images.ubuntu.com/minimal/releases/focal/release-20231208/ubuntu-20.04-minimal-cloudimg-amd64.img

echo "At this point, you will need to enter the username and password that will be used to create the virtual machine. 
You should subsequently use the same data to deploy the cluster."

echo "Enter username: "
read USERNAME

echo "Enter your password: "
read PASSWORD

FILESYSTEM = $(grep "path /var/lib/pve/" /etc/pve/storage.cfg | sed 's|^.*/||')

# Function to create a cloud-init template for a VM
create_cloud_init_template() {
    local vm_id=$1
    local memory=$2
    local cores=$3
    local name=$4
    local user=$5
    local password=$6

    echo "Creating a cloud-init template for $name VM"
    qm create $vm_id --memory $memory --core $cores --name $name --net0 virtio,bridge=vmbr0
    qm importdisk $vm_id ubuntu-20.04-minimal.img $FILESYSTEM
    qm set $vm_id --scsihw virtio-scsi-pci --scsi0 $FILESYSTEM:vm-$vm_id-disk-0
    qm set $vm_id --ide2 $FILESYSTEM:cloudinit
    qm set $vm_id --boot c --bootdisk scsi0
    qm set $vm_id --serial0 socket --vga serial0

    qm template $vm_id
    qm set $vm_id --ciuser $USERNAME --cipassword $PASSWORD --sshkeys sshkeys.pub \
    --ipconfig0 ip=dhcp
}

echo "Will the cluster be single-node (master and worker nodes - one virtual machine) or multi-node? (s/m): "
read clustermode

while true
    do
        if [ $clustermode = "s" ]; then
            #single-noded vm templates creation
            cat /root/.ssh/id_ed25519.pub /root/.ssh/ansible.pub >> sshkeys.pub
            create_cloud_init_template 2000 6144 3 "k3s-cluster-template" $USERNAME $PASSWORD
            create_cloud_init_template 2001 6144 2 "ptero-wings-template" $USERNAME $PASSWORD
            rm -f sshkeys.pub
            break

        elif [ $clustermode = "m" ]; then
            #multi-noded vm templates creation
            cat /root/.ssh/id_ed25519.pub /root/.ssh/ansible.pub >> sshkeys.pub
            create_cloud_init_template 2000 2048 1 "k3s-master-template" $USERNAME $PASSWORD
            create_cloud_init_template 2001 6144 3 "k3s-worker-template" $USERNAME $PASSWORD
            create_cloud_init_template 2002 6144 2 "ptero-wings-template" $USERNAME $PASSWORD
            rm -f sshkeys.pub
            break
        
        else
            echo "Wrong input! (s/m): "
            read clustermode
        fi
    done