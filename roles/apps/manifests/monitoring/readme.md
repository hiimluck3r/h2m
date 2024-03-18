# Monitoring Stack
### Related files and folders
* roles/apps/manifests/monitoring
* roles/apps/tasks/monitoring.yml

### Description
Installs the Kube-Prometheus monitoring stack, a collection of Kubernetes manifests, dashboards, and combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus using the Prometheus Operator.

More on https://github.com/prometheus-operator/kube-prometheus

### Credentials
* Username: admin
* Password: *password you entered in the configuration*

## Known Issues
Grafana is accessible only with 'monitoring-grafana' subdomain if not using specific HTTProute (as pagenotfound does).

Possible fix: use specified httproute definition

### Available on
* https://monitoring-grafana.yourdomain.com