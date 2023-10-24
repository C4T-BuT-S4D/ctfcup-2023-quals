#!/bin/bash

set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/more_heap
cd $pubtemp

zip -r more_heap.zip more_heap

cd $curdir
mv $pubtemp/more_heap.zip public

rm -rf $pubtemp