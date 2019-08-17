#|/bin/bash
################################################################
# Adding Planck LikelyHood and data
#ADD http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_Likelihood_Code-v3.0_R3.01.tar.gz /home/cosmos/planck_2018/
DIR="/home/cosmos/planck_2018"
CFITSIODIR="/opt/cfitstio"

export LD_LIBRARY_PATH="/opt/cfitsio/lib/:$LD_LIBRARY_PATH"

sudo chown -R cosmos:cosmos $DIR
cd $DIR
tar vxfz product-action
rm product-action
cd $DIR
cd ./code/plc_3.0/plc-3.01
python waf configure --install_all_deps --cfitsio_prefix=/opt/cfitsio
./waf install
cd bin/
source ./clik_profile.sh
