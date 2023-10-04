#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/web-scanner
cd $pubtemp

zip -9 -r web-scanner.zip web-scanner

cd $curdir
mv $pubtemp/web-scanner.zip public
rm -rf $pubtemp
