#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/ella_enchanted
cd $pubtemp

zip -9 -r ella_enchanted.zip ella_enchanted

cd $curdir
mv $pubtemp/ella_enchanted.zip public
rm -rf $pubtemp
