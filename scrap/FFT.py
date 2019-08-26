# https://www.oreilly.com/library/view/elegant-scipy/9781491922927/ch04.html
# https://martinos.org/mne/stable/auto_examples/time_frequency/plot_compute_raw_data_spectrum.html
# http://gael-varoquaux.info/scipy-lecture-notes/intro/scipy.html#fast-fourier-transforms-scipy-fftpack
# https://www.elenacuoco.com/2016/09/22/power-spectral-density/
# https://joseph-long.com/writing/from-sky-coordinates-to-pixels-and-back/
#
# https://www.datascience.com/learn-data-science/fundamentals/introduction-to-anomaly-detection-python-data-science
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
