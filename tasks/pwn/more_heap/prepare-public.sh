#!/bin/bash

set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cd deploy/
docker build -f build.Dockerfile -t build-more-heap .
docker run --name build-more-heap-1 build-more-heap
docker cp build-more-heap-1:/build/vuln .
docker rm build-more-heap-1
docker rmi build-more-heap

cd $curdir
mkdir -p $pubtemp/more-heap
cp deploy/vuln solve/
cp deploy/vuln $pubtemp/more-heap
cp deploy/Dockerfile $pubtemp/more-heap


cd $pubtemp
zip -r more-heap.zip more-heap

cd $curdir
mv $pubtemp/more-heap.zip public/

rm -rf $pubtemp