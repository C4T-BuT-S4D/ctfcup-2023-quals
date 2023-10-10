#!/bin/bash

set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cd deploy/
docker build -f build.Dockerfile -t build-some_storage .
docker run --name build-some_storage-1 build-some_storage
docker cp build-some_storage-1:/build/vuln .
docker rm build-some_storage-1
docker rmi build-some_storage

cd $curdir
mkdir -p $pubtemp/some_storage
cp deploy/vuln solve/
cp deploy/vuln $pubtemp/some_storage
cp deploy/Dockerfile $pubtemp/some_storage


cd $pubtemp
zip -r some_storage.zip some_storage

cd $curdir
mv $pubtemp/some_storage.zip public/

rm -rf $pubtemp