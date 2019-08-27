https://ourcodingclub.github.io/2019/01/07/pandas-time-series.html
https://bicorner.com/2015/11/16/time-series-analysis-using-ipython/
http://exnumerus.blogspot.com/2011/12/how-to-remove-noise-from-signal-using.html

https://timsainburg.com/noise-reduction-python.html
# https://www.oreilly.com/library/view/elegant-scipy/9781491922927/ch04.html

# http://gael-varoquaux.info/scipy-lecture-notes/intro/scipy.html#fast-fourier-transforms-scipy-fftpack


#
#
# http://python4mpia.github.io/core/core.html
#
# https://github.com/janerigby/astro-pandas-tutorials

# import jrr
import seaborn as sns
from astropy.io import ascii
from astropy.table import Table
from astropy.io import fits
from astropy.utils.data import download_file
from astropy.stats import mad_std
import pandas

mastercat_file = (
    "http://monoceros.astro.yale.edu/RELEASE_V4.1.5/3dhst.v4.1.5.master.fits.gz"
)
pmcat = Table.read(mastercat_file).to_pandas()

print(type(pmcat))
pandas.set_option('display.max_columns', 500)  # print all columns in .head()
pmcat.shape


# Demo some basic filtering.  Not used below.
zlo = 2.0
zhi = 3.0
Mlo = 9.0
Mhi = 9.5
print(pmcat[pmcat['use_phot'].eq(1)].shape)   # filter on good photometry
print(pmcat[pmcat['z_best'].between(zlo,zhi)].shape)  # Filter redshift
print(pmcat[pmcat['lmass'].between(Mlo,Mhi)].shape)   # Filter stellar mass
filt = pmcat['z_best'].between(zlo,zhi) & pmcat['lmass'].between(Mlo,Mhi) & pmcat['use_phot'].eq(1)
print(pmcat[filt].shape) #all 3 filters

# Read in Arjen's catalogs of morphological parameters, for each field
#download_file("http://www.mpia-hd.mpg.de/homes/vdwel/allfields.tar")
# below is really kludgy.  Did by hand
# mkdir VanderWel; cd VanderWel; mv ../allfields.tar . ; tar -xvf allfields.tar
# I then edited by hand the headers, stripping out the initial "#  "
vdw_H_files = ("VanderWel/aegis/aegis_3dhst.v4.1_f125w.galfit", "VanderWel/goodss/goodss_3dhst.v4.1_f125w.galfit", "VanderWel/cosmos/cosmos_3dhst.v4.1_f125w.galfit", "VanderWel/uds/uds_3dhst.v4.1_f125w.galfit", "VanderWel/goodsn/goodsn_3dhst.v4.1_f125w.galfit")
vdw_fields = ('aegis', 'goodss', 'cosmos', 'uds', 'goodsn')
vdw_df = {}
for ii, label in enumerate(vdw_fields):
    #jrr.util.strip_pound_before_colnames(vdw_H_files[ii])  # strip # from header
    vdw_df[label] = pandas.read_table(vdw_H_files[ii], delim_whitespace=True, comment="#", header=0)
    vdw_df[label]['field'] = vdw_fields[ii]
    vdw_df[label]['JRRID'] = vdw_fields[ii] + '.' + vdw_df[label]['NUMBER'].astype(str)
vdw_all = pandas.concat(vdw_df)


pmcat_jrr   = pmcat.set_index('JRRID', drop=False)
vdw_all_jrr= vdw_all.set_index('JRRID', drop=False)
pmcat_jrr.to_csv("pmcat.csv")
vdw_all_jrr.to_csv("vdw_alljrr.csv")


import pandas as pd
import io
import requests

url = "http://www.sidc.be/silso/DATA/SN_m_tot_V2.0.txt"
s = requests.get(url).content
ds = pd.read_csv(io.StringIO(s.decode('utf-8')))

ds.describe()
ds.head(5)
