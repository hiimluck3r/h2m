# Pagenotfound
### Related files and folders
* roles/apps/manifests/pagenotfound
* roles/apps/tasks/pagenotfound.yml

### Description
Sets up a 404 page with a wildcard, which is used as 404 page replacement. It's not perfect solution and not recommended for use in production environment, but it's fine for homelab because of it's simplicity.

Actually it's just a regular nginx webserver with custom index.html.

### Available on
* https://randomsubdomainthatdoesntexist.yourdomain.com