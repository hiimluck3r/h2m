import os
import yaml
import subprocess

print("""
██╗  ██╗██╗██╗███╗   ███╗                
██║  ██║██║██║████╗ ████║                
███████║██║██║██╔████╔██║                
██╔══██║██║██║██║╚██╔╝██║                
██║  ██║██║██║██║ ╚═╝ ██║                
╚═╝  ╚═╝╚═╝╚═╝╚═╝     ╚═╝                
                                         
██╗      █████╗ ██████╗  ██████╗ ███████╗
██║     ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║     ███████║██████╔╝██║   ██║███████╗
██║     ██╔══██║██╔══██╗██║   ██║╚════██║
███████╗██║  ██║██████╔╝╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝
--------
Created by @hiimluck3r
https://github.com/hiimluck3r/h2m
""")
user = input("Enter username (this username will be used for creating new nodes and for specific services): ")
domain = input("Enter domain of the cluster: ")
email = input("Enter your email: ")
password = input("Enter your password (this password will be used to manage some of the services): ")

print(f"User: {user}")
print(f"Domain: {domain}")
print(f"E-mail: {email}")
print(f"Password: {password}")

confirmation = input("Proceed? (y/n): ")
if confirmation != "y":
    print("Aborting the process...")
    exit()

while True:
    print("""
    ***
    Single-node: master and worker are on the same node
    Multi-node: master and worker have different nodes
    ***
    """)
    cluster_mode = input("Will the k3s cluster be single-node or multi-node? (s/m): ")
    if cluster_mode in ["s", "m"]:
        break
    else:
        print('Use "s" for single-node or "m" for multi-node as an answer string.')

master_nodes = []
worker_nodes = []
ptero_nodes = []
singlenode = [] #dumb, bad idea, but it works

if cluster_mode == "s":
    singlenode.append(input("Enter the IP of the cluster node: "))
else:
    while True:
        try:
            master_nodes_amount = int(input("How many master nodes do you want? Enter odd number: "))
            if (master_nodes_amount%2 == 0) or (master_nodes_amount <= 0):
                print(f"The amount of master nodes cannot equal to {master_nodes_amount}. Odd number of nodes is required for quorum.")
            else:
                for i in range(master_nodes_amount):
                    master_nodes.append(input(f"{i+1}. Enter the IP of master node: "))
                break
        except Exception as e:
            print(f"Exception found at the master node creation: {e}")
            exit()
    
    while True:
        try:
            worker_nodes_amount = int(input("How many worker nodes do you want: "))
            if (worker_nodes_amount <= 0):
                print(f"The amount of worker nodes cannot be equal to {worker_nodes_amount}.")
            else:
                for i in range(worker_nodes_amount):
                    worker_nodes.append(input(f"{i+1}. Enter the IP of worker node: "))
                break
        except Exception as e:
            print(f"Exception found at the worker node creation: {e}")
            exit()

while True:
    try:
        ptero_nodes_amount = int(input("How many ptero nodes do you want: "))
        for i in range(ptero_nodes_amount):
            ptero_nodes.append(f"{i+1}. Enter the IP of ptero node: ")
        break
    except Exception as e:
        print(f"Exception found at the ptero node creation: {e}")
        exit()

cp_vip = "" #Control-plane Virtual IP
if len(master_nodes) > 1:
    cp_vip = input("Enter free IP that will be used for Control-Plane LoadBalancer. It must be different from the IPs you entered above: ")

#Service LoadBalancer IP range
cidr_default = input("Enter CIDR-based IP range (192.168.0.10/29 where /29 is subnet mask 255.255.255.248): ")

newline = '\n'

print("""
---
Creating ansible-inventory
""")

with open("inventory", "w") as inv_file:
    inv_file.write("[master]\n")
    for each in master_nodes:
        inv_file.write(f"{each}\n")
    
    inv_file.write("\n[worker]\n")
    for each in worker_nodes:
        inv_file.write(f"{each}\n")
    
    inv_file.write(f"\n[cluster]\n")
    for each in singlenode:
        inv_file.write(f"{each}\n")

    inv_file.write(f"\n[wings]\n")
    for each in ptero_nodes:
        inv_file.write(f"{each}\n")

    inv_file.write(f"""\n[k3c:children]
master
worker
cluster
""")

with open("group_vars/all/h2mcfg.yml", 'w') as sys_file:
    sys_file.write(f"""---
master_nodes: {master_nodes_amount}
cp_vip: {cp_vip} #Control-plane Virtual IP
cidr_default: {cidr_default} #CIDR-based kube-vip LoadBalancer IP range
domain: {domain}
user: {user}
""")

with open("group_vars/all/vault.yml", 'w') as sys_file:
    sys_file.write(f"""---
email: {email}
password: {password}
""")

vault_encrypt = subprocess.call(["ansible-vault", "encrypt", "group_vars/all/vault.yml"])

print("Don't forget this password since it's the only way of decrypting secrets you provided before.")