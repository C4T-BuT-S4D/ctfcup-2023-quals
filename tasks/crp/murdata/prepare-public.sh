#!/bin/bash

set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/crp-murdata
cp public.env $pubtemp/crp-murdata/app.env
cd $pubtemp

zip -9 -r crp-murdata.zip crp-murdata

cd $curdir
mv $pubtemp/crp-murdata.zip public
rm -rf $pubtemp
