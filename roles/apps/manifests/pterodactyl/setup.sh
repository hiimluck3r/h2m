#!/bin/bash

#./setup.sh firstname lastname email password username
kubectl cp panel.conf $(kubectl get pods | grep kubectyl-panel | awk '{print $1}'):/etc/nginx/http.d/ --;
kubectl exec $(kubectl get pods | grep kubectyl-panel | awk '{print $1}') -- php artisan p:user:make --admin=1 --name-first="$1" --name-last="$2" --email="$3" --password="$4" --username="$5";
kubectl delete pod $(kubectl get pods | grep kubectyl-panel | awk '{print $1}');