#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

echo $pubtemp

cp -R deploy $pubtemp/mistakes
cd $pubtemp

sed -r -i '' 's/ctfcup\{[^}]+\}/ctfcup{fake_flag}/g' mistakes/docker-compose.yaml

zip -9 -r task.zip mistakes

cd $curdir
mv $pubtemp/task.zip public/
rm -rf $pubtemp