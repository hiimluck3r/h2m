#!/bin/bash

#usage example: ./uploadbook.sh /books/LinuxBible https://sitewithyourbook.com/ linuxbible.pdf
kubectl exec -it $(kubectl get pods | grep kavita | awk '{print $1}') -- mkdir -p $1;
kubectl exec -it $(kubectl get pods | grep kavita | awk '{print $1}') -- curl $2 -o $1/$3;