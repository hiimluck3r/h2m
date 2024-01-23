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
    k3version = input("Will you use k3s or k3d? (k3s/k3d): ")
    if k3version in ["k3d", "k3s"]:
        break
    else:
        print('Use "k3s" or "k3d" as an answer string.')

while True:
    print("""
    ***
    Single-node: master and worker are on the same node
    Multi-node: master and worker have different nodes
    ***
    """)
    cluster_mode = input("Will the cluster be single-node or multi-node? (s/m): ")
    if cluster_mode in ["s", "m"]:
        break
    else:
        print('Use "s" for single-node or "m" for multi-node as an answer string.')

master_nodes = []
worker_nodes = []
ptero_nodes = []
singlenode = ""

if cluster_mode == 'm':
    while True:
        try:
            master_node_count = int(input("How many master nodes will you use? (Preferably 1 or 3): "))
            if master_node_count <= 0:
                raise Exception("You can't create a cluster without master-nodes")
            print("Enter master-nodes IPs:")
            for i in range(master_node_count):
                master_nodes.append(input(f"Master-node ({i}): "))
            break
        except Exception as e:
            print(f"Found an exception at the master-node creation: {e}\n")
    
    while True:
        try:
            worker_node_count = int(input("How many worker nodes will you use?: "))
            if worker_node_count <= 0:
                raise Exception("You can't create a cluster without worker-nodes")
            print("Enter worker-nodes IPs:")
            for i in range(worker_node_count):
                worker_nodes.append(input(f"Worker-node ({i}): "))
            break
        except Exception as e:
            print(f"Found an exception at the worker-node creation: {e}\n")

    while True:
        try:
            ptero_node_count = int(input("How many pterodactyl nodes (wings) will you use?: "))
            if worker_node_count < 0:
                raise Exception("You can't create a cluster with ptero-nodes below zero")
            elif worker_node_count > 0:
                print("Enter ptero-nodes IPs:")
            for i in range(worker_node_count):
                worker_nodes.append(input(f"Ptero-node ({i}): "))
            break
        except Exception as e:
            print(f"Found an exception at the ptero-node creation: {e}\n")

else:
    singlenode = input("Enter kubernetes-node IP: ")
    while True:
        try:
            ptero_node_count = int(input("How many pterodactyl nodes (wings) will you use?: "))
            if ptero_node_count < 0:
                raise Exception("You can't create a cluster with ptero-nodes below zero")
            elif ptero_node_count > 0:
                print("Enter ptero-nodes IPs:")
            for i in range(ptero_node_count):
                ptero_nodes.append(input(f"Ptero-node ({i}): "))
            break
        except Exception as e:
            print(f"Found an exception at the ptero-node creation: {e}\n")

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
    
    inv_file.write(f"\n[cluster]\n{singlenode}\n")

    inv_file.write(f"\n[wings]\n")
    for each in ptero_nodes:
        inv_file.write(f"{each}\n")

with open("group_vars/all/vault.yml", 'w') as sys_file:
    sys_file.write(f"""---
k3v: {k3version}
user: {user}
domain: {domain}
email: {email}
password: {password}
""")

vault_encrypt = subprocess.call(["ansible-vault", "encrypt", "group_vars/all/vault.yml"])

print("Don't forget this password since it's the only way of decrypting secrets you provided before.")