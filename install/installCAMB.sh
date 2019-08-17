#!/bin/bash
# Installing CAMB from git
git clone https://github.com/cmbant/CAMB.git --recursive && \
cd CAMB && \
git checkout && \
export PATH="/usr/bin:$PATH"
source activate cosmos3
python setup.py install
