# GitLab Runner
### Related files and folders
* roles/apps/manifests/gitlab-runner
* roles/apps/tasks/gitlab_runner.yml
* roles/apps/templates/gitlab-runner-values.yaml.j2

### Description
GitLab Runner runs the CI/CD jobs that are defined in GitLab.

More on https://docs.gitlab.com/runner/install/

### Credentials
You need to provide the following information in config/apps_cfg.yml (to use as default) or in group_vars/all/h2mcfg.yml (for specific configuration):

```yaml
#gitlab-runner
runners:
   - project1|TOKEN1|https://gitlab.com
   - project2|TOKEN2|https://gitlab.com
   - project3|TOKEN3|https://gitlab.com
```

Where:
* Project is the name of instance to easily distinguish multiple gitlab-runner instances
* TOKEN is your GitLab project/group/server runner token
* URL is your GitLab server