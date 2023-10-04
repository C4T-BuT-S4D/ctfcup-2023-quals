#!/bin/bash

echo "$FLAG" > /flag
FLAG=""

/usr/bin/supervisord -c /supervisord.conf
