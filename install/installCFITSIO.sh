#!/bin/bash
# # Installing CFITSIO system wide
# Shared option is needed by planck likelyhood
DIR="/opt/cfitsio"
# ADD http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz /tmp
# WORKDIR /tmp
cd /tmp/
tar xvf cfitsio-3.47.tar.gz
cd /tmp/cfitsio-3.47
./configure --prefix=$DIR
make shared
make install
cd /tmp
rm cfitsio-3.47.tar.gz
rm -fr cfitsio-3.47
