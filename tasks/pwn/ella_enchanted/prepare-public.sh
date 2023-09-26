#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/ella_enchanted
cd $pubtemp

sed -i -r 's/ctfcup\{[^}]+\}/ctfcup{fake_flag}/g' ella_enchanted/flag.txt
zip -9 -r ella_enchanted.zip ella_enchanted

cd $curdir
mv $pubtemp/ella_enchanted.zip public
rm -rf $pubtemp
