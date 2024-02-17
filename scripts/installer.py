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
while True:
    if len(password) < 10:
        password = input("Weak password! Use 10 to 32 characters: ")
    elif len(password) > 32:
        password = input("Too much! Use 10 to 32 characters: ")
    else:
        break

print(f"User: {user}")
print(f"Domain: {domain}")
print(f"E-mail: {email}")
print(f"Password: {password}") #should you even see it?

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
        
        #for now
        if cluster_mode == "m":
            print("Multi-node mode is currently unavailable.")
            exit()

        break
    else:
        print('Use "s" for single-node or "m" for multi-node as an answer string.')

master_nodes = []
worker_nodes = []
singlenode = ""

if cluster_mode == "s":
    singlenode = input("Enter the IP of the cluster node: ")
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

cp_vip = "" #Control-plane Virtual IP
if len(master_nodes) > 1:
    cp_vip = input("Enter free IP that will be used for Control-Plane LoadBalancer. It must be different from the IPs you entered above: ")

#Service LoadBalancer IP range
cidr_global = input("Enter CIDR-based IP range (192.168.0.10/29 where /29 is subnet mask 255.255.255.248): ")

kube_vip_interface = input("Enter network inteface that KubeVip will bind to: ")

newline = '\n'

print("""
---
Creating ansible-inventory
""")

#I want to refactor it so badly
#Please, try to implement newline with jinja-ish templating using f-strings
with open("../inventory", "w") as inv_file:
    inv_file.write(f"""[leader]
{master_nodes[0] if len(master_nodes)!=0 else ""}

[quorum]
{newline.join(master_nodes[1::])}

[master]
leader
quorum

[cluster]
{singlenode}

[worker]
{newline.join(worker_nodes)}

[k3c:children]
master
cluster""")

with open("../group_vars/all/h2mcfg.yml", 'w') as sys_file:
    sys_file.write(f"""---
cp_vip: {cp_vip} #Control-plane Virtual IP
cidr_global: {cidr_global} #CIDR-based kube-vip LoadBalancer IP range
domain: {domain}
user: {user}
kube_vip_interface: {kube_vip_interface}
kube_vip_version: v0.6.4

#Applications
ghostUsername: user
ghostBlogTitle: h2m Blog
ghostEnableHttps: false

""") #kube_vip_version 0.6.4 is stable

with open("group_vars/all/vault.yml", 'w') as sys_file:
    sys_file.write(f"""---
email: {email}
password: {password}
""")

vault_encrypt = subprocess.call(["ansible-vault", "encrypt", "group_vars/all/vault.yml"])

print("Don't forget this password since it's the only way of decrypting secrets you provided before.")