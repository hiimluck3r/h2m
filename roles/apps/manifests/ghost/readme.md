# Ghost
### Related files and folders
* roles/apps/manifests/ghost
* roles/apps/tasks/ghost.yml
* config/ghost_cfg.yml

### Description
Ghost is a powerful app for professional publishers to create, share, and grow a business around their content. It comes with modern tools to build a website, publish content, send newsletters & offer paid subscriptions to members. 

More on https://ghost.org/docs/

### Careful, the data
As with any other PVC with StorageClass with a Delete policy, all data is deleted when the deployment is removed, so be sure to back up all existing data if you want to disable this service.

### Credentials
* Username: *email you entered in the configuration*
* Password: *password you entered in the configuration*

## Known Issues
Ghost Web-app container is known to fall a bunch of times while trying to connect to mysql database. It's an issue related to bitnami mysql image, which is trying to upgrade itself any time the pod is loaded. For now, you can wait until database is loaded. 

Possible fix: change mysql image.

### Available on
* https://ghost.yourdomain.com