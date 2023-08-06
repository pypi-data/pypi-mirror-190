#!/bin/bash

export LHAPDF_ROOT_DIR=/software/lhapdf-install
export LD_LIBRARY_PATH=/usr/local/lib/python3.10/dist-packages/nudisxs:$LD_LIBRARY_PATH

pip install numpy matplotlib

pip install nudisxs
