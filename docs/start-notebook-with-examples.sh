#!/bin/bash
set -e

if [ ! -d ~/work/examples ]; then
  mkdir ~/work/examples
  cp /forge/docs/examples/*.ipynb ~/work/examples/
fi

if [ ! -d ~/work/tutorials ]; then
  mkdir ~/work/tutorials
  cp /forge/docs/tutorials/*.ipynb ~/work/tutorials/
fi


. /usr/local/bin/start.sh jupyter notebook $*
