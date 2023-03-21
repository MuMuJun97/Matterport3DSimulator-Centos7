#!/bin/bash

echo -e "Python version: $(python --version)"

# ENV
export MPDIR=$(pwd)

python extra/env.py

export PKG_CONFIG_EXECUTABLE=$MPDIR/extra/pkgconfig/bin/pkg-config:$PKG_CONFIG_EXECUTABLE
export PATH=$MPDIR/extra/pkgconfig/bin:$PATH
export PKG_CONFIG_PATH=$MPDIR/extra:$PKG_CONFIG_PATH

echo "Finished!"
