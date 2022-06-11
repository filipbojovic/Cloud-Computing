#!/bin/bash
# docker pull mysql:latest
path=`pwd`
mysql_init_path="$path/MySQL/init"
mysql_storage_path="$path/MySQL/storage"
docker run -e MYSQL_ROOT_PASSWORD=fika -p 10000:3306 -v $mysql_init_path:/docker-entrypoint-initdb.d -v $mysql_storage_path:/var/lib/mysql -t mysql:latest
