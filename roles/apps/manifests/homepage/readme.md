# Homepage
### Related files and folders
* roles/apps/manifests/homepage
* roles/apps/tasks/homepage.yml
* roles/apps/templates/homepage-values.yaml.j2

### Description
A modern, fully static, fast, secure fully proxied, highly customizable application dashboard with integrations for over 100 services and translations into multiple languages. Easily configured via YAML files or through docker label discovery. 

More on https://gethomepage.dev/

### Configuration
Edit the following information in `config/apps_cfg.yml` (to use as default) or in `group_vars/all/h2mcfg.yml` (for specific configuration):

```yaml
#homepage
homepage_subdomain: homepage
homepage_settings_yaml: |
  ---
  providers:
    openweathermap: openweathermapapikey
    weatherapi: weatherapiapikey

homepage_widgets_yaml: |
  ---
  - resources:
      cpu: true
      memory: true
      disk: /
  - search:
      provider: duckduckgo
      target: _blank

homepage_services_yaml: |
  ---
  - Arr:
    - My First Service:
        href: http://localhost/
        description: Homepage is awesome
  - Media:
    - My Second Service:
        href: http://localhost/
        description: Homepage is the best
  - Infra:
    - My Third Service:
        href: http://localhost/
        description: Homepage is cool

homepage_bookmarks_yaml: |
  ---
  - Developer:
      - Github:
          - abbr: GH
            href: https://github.com/
  - Social:
      - Reddit:
          - abbr: RE
            href: https://reddit.com/
  - Entertainment:
      - YouTube:
          - abbr: YT
            href: https://youtube.com/
  - Hiimluck3r:
      - Github:
        - abbr: GH
          href: https://github.com/hiimluck3r
          description: "hiimluck3r's GitHub"
```

For configuration options and examples, please see: https://gethomepage.dev/latest/configs/settings

### Available on
* https://homepage.yourdomain.com