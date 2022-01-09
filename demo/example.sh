#!/bin/bash

CURDIR=$(cd $(dirname $0); pwd)

echo "current directory $CURDIR"

export PATH=$CURDIR/..:$PATH
export PYTHONPATH=$CURDIR/..:$PYTHONPATH

python3 $CURDIR/example.py