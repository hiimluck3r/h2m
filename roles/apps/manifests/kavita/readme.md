# Kavita
### Related files and folders
* roles/apps/manifests/kavita
* roles/apps/tasks/kavita.yml

### Description
Kavita is a rocket fueled self-hosted digital library which supports a vast array of file formats. 

### Careful, the data
As with any other PVC with StorageClass with a Delete policy, all data is deleted when the deployment is removed, so be sure to back up all existing data if you want to disable this service.

### Credentials
You'll be prompted to create admin account after the installation.

### Book uploading
You have the following folders, located in root (/) directory:

* /books
* /manga
* /comics

Basically you need to create a folder with a file inside of it (.pdf, .epub, etc.)

I apply the **upload_books.sh** script to slightly automate the process. It might be automated even more with creating .txt with sources or whatever.

Usage example:

```bash
#inside of ~/manifests/kavita directory
./upload_books.sh /books/LinuxBible https://example.com/randomlinuxbook.pdf LinuxBible.pdf
```

Where 1st is the folder where the book will be located, 2nd is the url to download the file, 3rd is the file name.

There surely is better workaround, such as readarr, but I don't want to implement it (yet).

Insides of upload_book.sh:
```bash
#!/bin/bash

#usage example: ./uploadbook.sh /books/LinuxBible https://sitewithyourbook.com/ linuxbible.pdf
kubectl exec -it $(kubectl get pods | grep kavita | awk '{print $1}') -- mkdir -p $1;
kubectl exec -it $(kubectl get pods | grep kavita | awk '{print $1}') -- curl $2 -o $1/$3;
```

More on https://wiki.kavitareader.com/en

### Available on
* https://kavita.yourdomain.com