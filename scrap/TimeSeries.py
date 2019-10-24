#https://ourcodingclub.github.io/2019/01/07/pandas-time-series.html
#https://towardsdatascience.com/from-scratch-bayesian-inference-markov-chain-monte-carlo-and-metropolis-hastings-in-python-ef21a29e25a
#https://github.com/royalosyin/Python-Practical-Application-on-Climate-Variability-Studies
#http://www.das.inpe.br/school/2009/lectures_feigelson/INPE_Feigelson_R.pdf
#https://wwwmpa.mpa-garching.mpg.de/~ensslin/nifty-gallery/index.html

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.graphics.api import qqplot
import io
import requests
%matplotlib inline
##############
# Monthly data
url = "http://www.sidc.be/silso/DATA/SN_m_tot_V2.0.txt"
s = requests.get(url).content
colnames = ['YEAR', 'MONTH', 'YM', 'ACTIVITY', 'C1', 'C2', 'C3']
df = pd.read_table(io.StringIO(s.decode('utf-8')), names = colnames, header = None, delim_whitespace=True )
df.head(5)

df.shape
df.

df['DAY']=1
df = df[['YEAR', 'MONTH', 'DAY', 'ACTIVITY']]
df.index = pd.to_datetime(df[['YEAR','MONTH','DAY']])
df = df[['ACTIVITY']]
df.head(5)
df.info()
df.describe()
pd.to_datetime(df[['YEAR','MONTH','DAY']])
# You can select by datetime with partial match
df.loc['1830']
#############
import seaborn as sns
# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
df['ACTIVITY'].plot(linewidth=0.5);

df = df.asfreq('M', method='ffill')
df_year = df.resample('Y').mean()
df_year.head(3)


# Compute the centered 7-day rolling mean
df_5y = df_year['ACTIVITY'].rolling(5, center=True).mean()
df_5y.head(10)


# Start and end of the date range to extract
#start, end = '1780-01', '2017-06'
# Plot daily, weekly resampled, and 7-day rolling mean time series together
fig, ax = plt.subplots()
ax.plot(df,
linestyle='-', linewidth=0.5, color = "red", alpha = 0.5, label='Monthly')
ax.plot(df_year,
marker='.', linestyle='-', linewidth=0.5, label='Yearly')
ax.plot(df_5y,
marker='o', markersize=4, linestyle='-', label='Moving Window')
ax.set_ylabel('Solar Activity')
ax.legend();


df.loc['1900':'1990'].resample("5y").median().diff().plot()

pd.plotting.autocorrelation_plot(df.resample("1y").median())


file = "../DATA/co2_mm_mlo.txt"
colnames = ["year", "month", "decimal_date", "average", "interpolated", "trend", "days"]
df = pd.read_table( file,
                    names = colnames,
                    header = None,
                    delim_whitespace=True,
                    comment = '#',
                    skiprows = 72,
                    na_values = [-99.99, -1] )
df.head(3)

df['Date'] = df['year']*100 + df['month']
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m', errors='ignore')
df.set_index('Date', inplace=True)
df.drop(["year", "month", "decimal_date", "interpolated",  "trend", "days"], axis=1, inplace=True)
df.head(3)

df.isnull().sum()
# Filling missing values
df = df.fillna(df.bfill())
df.plot(title='Monthly CO2 (ppm)')

# Decompose do not handle missing values
decomposition = sm.tsa.seasonal_decompose(df, model='additive')
fig = decomposition.plot()


df_seasonal = decomposition.seasonal.asfreq('M', method='ffill')
df_seasonal.head(3)


pd.plotting.autocorrelation_plot(df_seasonal)
plt.xlim([0,24])


from scipy import signal

n        = 100
alpha    = 1
noverlap = 50
nfft     = 1024 #default value
fs       = 1   #default value
win      = signal.tukey(n, alpha)
data     = df_seasonal['average'].values # convert vector

f1, pxx1  = signal.welch(data, nfft=nfft, fs=fs, window=win, noverlap=noverlap)

# process frequencies and psd
pxx1 = pxx1/np.max(pxx1) # normalize the psd values
plt.plot(1.0/f1, pxx1, label='welch')
plt.title('CO2 Spectrum via welch');
plt.xlabel('Months')
plt.xlim([0,24])


#https://hadrienj.github.io/posts/Preprocessing-for-deep-learning/

https://hub.gke.mybinder.org/user/elegant-scipy-notebooks-yqah45st/notebooks/notebooks/ch3.ipynb
https://hub.gke.mybinder.org/user/elegant-scipy-notebooks-yqah45st/notebooks/notebooks/ch4.ipynb
http://gael-varoquaux.info/scipy-lecture-notes/intro/scipy.html#fast-fourier-transforms-scipy-fftpack
