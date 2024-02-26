# Castopod
### Related files and folders
* roles/apps/manifests/castopod
* roles/apps/tasks/castopod.yml
* config/castopod_env.yml

### Description
Castopod is a free and open-source solution to your podcasting.
Self-host your podcasts with ease, keep control over what you create and talk to your audience without any middleman. Your podcast and your audience belong to you and you only.

More on https://docs.castopod.org

### Careful, the data
As with any other PVC with StorageClass with a Delete policy, all data is deleted when the deployment is removed, so be sure to back up all existing data if you want to disable this service.

### Credentials
Create your admin after the installation on https://castopod.domain.com/cp-install

## Known Issues
Redis and MariaDB passwords not secured in vault.yml.

Possible fix: using secrets is useless if passwords are shown in env. To be explored.

### Available on
* https://castopod.yourdomain.com