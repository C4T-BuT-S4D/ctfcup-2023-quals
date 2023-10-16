#!/usr/bin/env bash

echo $FLAG > /flag.txt

socat "TCP-LISTEN:13000,reuseaddr,fork" "EXEC:/task"
