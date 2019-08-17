#!/usr/bin/env bash
# installing  COSMOSIS
git clone http://bitbucket.org/joezuntz/cosmosis
cd /home/cosmos/cosmosis
git checkout
git clone http://bitbucket.org/joezuntz/cosmosis-standard-library
cd /home/cosmos/cosmosis
cp /tmp/setup-my-cosmosys /home/cosmos/cosmosis/setup-my-cosmosis
source activate cosmos3
source setup-my-cosmosis
make
