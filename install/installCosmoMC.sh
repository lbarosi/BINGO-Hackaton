#!/bin/bash
# Install COSMOMC
git clone --recursive https://github.com/cmbant/CosmoMC.git
cd CosmoMC
git checkout
source activate cosmos3
source /home/cosmos/planck_2018/code/plc_3.0/plc-3.01/bin/clik_profile.sh
export PATH="/usr/bin:$PATH"
ln -s /home/cosmos/planck_2018/baseline/plc_3.0 ./data/clik_14.0 && \
make
