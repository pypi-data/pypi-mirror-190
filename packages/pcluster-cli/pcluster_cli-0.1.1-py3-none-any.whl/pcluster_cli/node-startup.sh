#!/bin/bash
mkdir -p /var/scripts

printf "#!/bin/bash \n\
rm -rf /var/backup\n\
mkdir -p /var/backup\n\
mv /etc/munge/munge.key /home/ec2-user/.munge /var/spool/slurm.state/clustername /etc/parallelcluster/ /var/backup \n\
mkdir  /etc/parallelcluster/ && cp /var/backup/parallelcluster/image_dna.json /etc/parallelcluster/" > /var/scripts/backup-start.sh


printf "#!/bin/bash \n\
mv /var/backup/munge.key /etc/munge/munge.key \n\
mv /var/backup/.munge /home/ec2-user/.munge \n\
mv /var/backup/clustername /var/spool/slurm.state/clustername \n\
rm -rf /etc/parallelcluster && mv /var/backup/parallelcluster/ /etc/parallelcluster" > /var/scripts/backup-complete.sh


chmod +x /var/scripts/backup-start.sh /var/scripts/backup-complete.sh

if [ $# -le 1 ]; then
   exit 0
fi

if [ -n "$(command -v s3fs)" ]; then
   echo "s3fs present in the system"
else
   echo "installing s3fs"
   if [ -n "$(command -v yum)" ]; then
      yum install s3fs-fuse -y
   else
      apt update -y
      apt install s3fs -y
   fi
fi
ds_path="/datasets"

mkdir -p $ds_path
chmod +777 $ds_path
su -c 'echo "user_allow_other" > /etc/fuse.conf'
arr=($( awk -F',' '{ for( i=1; i<=NF; i++ ) print $i }' <<< "$2"))
mounts=($(ls $ds_path))
for item in "${mounts[@]}"; do
   if [[ ${arr[*]} =~ (^|[[:space:]])$item($|[[:space:]]) ]]; then
      echo "mount is already present";
   else
      umount -f $ds_path/$item
      rm -rf $ds_path/$item
   fi
done

for item in "${arr[@]}"; do
      if [ -d "$ds_path/$item" ]
      then
          echo "already mounted $item"
      else
         mkdir -p  $ds_path/$item
         s3fs $item $ds_path/$item -o "iam_role=auto,umask=0022,allow_other" &
      fi
done
