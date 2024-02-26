<h1 align="center" id="title">h2m</h1>

<p align="center"><img src="pictures/h2mlogo.jpg" width ="200" height ="200" alt="project-image"></p>

<p id="description">Ansible-configured Homelab with k3s cluster inside a Proxmox VM.
</p>

<h2>⏳ Current project state:</h2>

Currently **h2m** is a single-node **K3S** cluster, with **kube-vip-cloud-provider** and **Kong Gateway API** (Kong Ingress Controller) for communicating with nodes, provisioned with **Ansible**.

Available set of applications:

* HTTP servers (nginx, apache)
* NextCloud
* LittleLink
* Kavita
* Ghost
* Castopod

And also monitoring with:

* Prometheus
* Grafana

<h2>🎯 Roadmap:</h2>

* HA Cluster with multiple VMs
* Kube-VIP master load balancing
* More services! (Gitea, Gitlab, Mailu, etc.)

<h2>🛠️ Installation Steps:</h2>

<p><strong>0. Pre-configure your PVE node</strong></p>
Create a non-root user on whose behalf the following commands will be executed:

```bash
adduser h2m
```
Give sudo access to created user:

```bash
usermod -aG wheel h2m
```

If you're not using enterprise Proxmox solution, then you'll probably want to get rid of "No subscription" pop-up as well as of updating your repositories to non-subscription ones.

You can do it yourself by changing following files:

* /etc/apt/sources.list.d/ceph.list
* /etc/apt/sources.list.d/pve-enterprise.list
* /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js

Or you might use configuration script.

Download the pve_init.sh script
```
curl https://raw.githubusercontent.com/hiimluck3r/h2m/dev/scripts/pve_init.sh -o pve_init.sh
```
Then launch it using

```bash
./pve_init.sh
```

**Please do not provide a password and passphrase for the Ansible ssh-key.**

**Install beaupy python library, it's crucial dependency for installation scripts**

```bash
apt install python3-pip

pip install beaupy --break-system-packages
```

<p><strong>1. Clone the repository</strong></p>

```bash
git clone https://github.com/hiimluck3r/h2m.git

cd h2m
```

If you want to use unstable **dev** branch:

```bash
git checkout dev
```

<p><strong>2. Configure virtual machines</strong></p>

Ansible tasks are intended to run on debian-based OS, preferably cloud-init.
You can manually create VMs, pass ansible keys to it and use your settings or you might use pre-configured VM templates, which are created using **vm_templates.sh** script.

```bash
cd scripts

./vm_templates.sh
```

After getting templates, go to your PVE dashboard and create full-clone virtual machine. You should also resize the virtual disk inside of GUI.

<p><strong>3. Run configuration script</strong></p>

```bash
./configure.sh
```

Later, if you want to configure which services to use, you can use

```bash
./services_cfg.sh
```

You can destroy your cluster with

```bash
./destroy.sh
```
---
<h3>Storage configuration</h3>

You can manage storage capacity for stateful applications in the following configs:

* config/storage_cfg.yml (main template)
* group_vars/all/h2mconfig.yml

<h2>🍰 Contribution Guidelines:</h2>

Contributions are what make the open source community such an amazing place to learn inspire and create. Any contributions you make are greatly appreciated. If you have a suggestion that would make this better please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

<h2>💻 Built with</h2>

Technologies used in the project:

*   Ansible
*   K3S
*   Python
*   Bash
*   Proxmox
*   k3sup

<h2>🛡️ License:</h2>

This project is licensed under the MIT License

<h2>🐛 Bugs or Questions:</h2>

Create an Issue with the appropriate tag:
* Feature request
* Bug report
* Question

<h2>💖Like my work?</h2>

Then give project a star :)