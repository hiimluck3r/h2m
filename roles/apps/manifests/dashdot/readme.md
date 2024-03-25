# dashdot
### Related files and folders
* roles/apps/manifests/dashdot
* roles/apps/tasks/dashdot.yml

### Description
dash. (or dashdot) is a modern server dashboard, running on the latest tech, designed with glassmorphism in mind. It is intended to be used for smaller VPS and private servers. 

More on https://getdashdot.com/

### Configuration
Edit the following information in `config/apps_cfg.yml` (to use as default) or in `group_vars/all/h2mcfg.yml` (for specific configuration):

```yaml
#dashdot
dashdot_subdomain: dashdot
DASHDOT_SHOW_HOST: false
DASHDOT_SHOW_VERSION: true
DASHDOT_ENABLE_CPU_TEMPS: false
DASHDOT_PAGE_TITLE: "dashdot."
DASHDOT_WIDGET_LIST: "os,cpu,storage,ram,network" #gpu is also available
DASHDOT_OS_LABEL_LIST: "os,arch,up_since"
DASHDOT_CPU_LABEL_LIST: "brand,model,cores,threads,frequency"
DASHDOT_STORAGE_LABEL_LIST: "brand,size,type"
DASHDOT_RAM_LABEL_LIST: "brand,size,type,frequency"
DASHDOT_NETWORK_LABEL_LIST: "type,speed_up,speed_down,interface_speed"
DASHDOT_GPU_LABEL_LIST: "brand, model, memory"
```

For configuration options and examples, please see: https://getdashdot.com/docs/configuration/basic

### Available on
* https://dashdot.yourdomain.com