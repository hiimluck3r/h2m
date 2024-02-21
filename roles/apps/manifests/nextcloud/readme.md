# NextCloud
### Related files and folders
* roles/apps/manifests/nextdcloud
* roles/apps/tasks/nextcloud.yml

### Description
Nextcloud is a suite of client-server software for creating and using file hosting services. Nextcloud provides functionality similar to Dropbox, Office 365 or Google Drive when used with integrated office suites Collabora Online or OnlyOffice. 

More on https://docs.nextcloud.com/

### Careful, the data
As with any other PVC with StorageClass with a Delete policy, all data is deleted when the deployment is removed, so be sure to back up all existing data if you want to disable this service.

### Credentials
* Username: *username you entered in the configuration*
* Password: *password you entered in the configuration*

### Available on
* https://nextcloud.yourdomain.com