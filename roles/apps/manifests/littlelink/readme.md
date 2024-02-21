# LittleLink
### Related files and folders
* roles/apps/manifests/littlelink
* roles/apps/tasks/littlelink.yml
* config/littlelink_env.yml
* scripts/littlelink_cfg.sh
* script/littlelink_cfg.py

### Description
LittleLink is an open source DIY Linktree alternative


## Setting up LittleLink
If using littlelink, run a special script to enable/disable specific social networks. 

```bash
./littlelink_cfg.sh
```

You can change the template to use your own links in **config/social.yml** (main template file) or in **group_vars/all/h2mconfig.yml** (filled in after running configure.sh or installer.py).

More on https://github.com/techno-tim/littlelink-server

### Available on
* https://littlelink.yourdomain.com