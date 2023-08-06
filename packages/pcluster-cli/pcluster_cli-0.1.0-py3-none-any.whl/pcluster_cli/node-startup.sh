#!/bin/bash

if [ $# -le 1 ]; then
   exit 0
fi

if [ -n "$(command -v s3fs)" ]; then
   echo "s3fs present in the system"
else
   echo "installing s3fs"
   if [ -n "$(command -v yum)" ]; then
      sudo yum install s3fs-fuse -y
   else
      sudo apt update -y
      sudo apt install s3fs -y
   fi
fi
ds_path="/datasets"

sudo mkdir -p $ds_path
sudo chmod +777 $ds_path
sudo su -c 'echo "user_allow_other" > /etc/fuse.conf'
arr=($( awk -F',' '{ for( i=1; i<=NF; i++ ) print $i }' <<< "$2"))
mounts=($(ls $ds_path))
for item in "${mounts[@]}"; do
   if [[ ${arr[*]} =~ (^|[[:space:]])$item($|[[:space:]]) ]]; then
      echo "mount is already present";
   else
      sudo umount -f $ds_path/$item
      rm -rf $ds_path/$item
   fi
done

for item in "${arr[@]}"; do
      if [ -d "$ds_path/$item" ]
      then
          echo "already mounted $item"
      else
         mkdir -p  $ds_path/$item
         sudo s3fs $item $ds_path/$item -o "iam_role=auto,umask=0022,allow_other" &
      fi
done
