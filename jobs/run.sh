#!/bin/bash

set -e

cd `dirname "$0"`

python launcher.py -n test -a write -p "this is a story"


sleep 10