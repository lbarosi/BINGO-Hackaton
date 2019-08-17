%pylab inline
pylab.rcParams['figure.figsize'] = 7, 7

from skyfield import api
from pytz import timezone
import numpy as np
import matplotlib.pyplot as plt
brasil = timezone('America/Recife')

GPSsats = api.load.tle('https://celestrak.com/NORAD/elements/gps-ops.txt')
exemplo = GPSsats["GPS BIIA-23 (PRN 18)"]
GLOsats = api.load.tle('https://celestrak.com/NORAD/elements/glo-ops.txt')
GALILEOsats = api.load.tle('https://celestrak.com/NORAD/elements/galileo.txt')
BEIDOUsats = api.load.tle('https://celestrak.com/NORAD/elements/beidou.txt')

BINGO = api.Topos(latitude = '7.05 S', longitude = '38.266 W')

minutes = range(60*24)
ts = api.load.timescale()
t = ts.utc(2019,9,1,0,minutes)
print(t)

orbit = (exemplo - BINGO).at(t)
alt, az, distance = orbit.altaz()

above_horizon = alt.degrees > 0
print(above_horizon)

indicies, = above_horizon.nonzero()
print(indicies)

boundaries, = np.diff(above_horizon).nonzero()
print(boundaries)

passes = boundaries.reshape(len(boundaries) // 2, 2)
print(passes)

def plot_sky(pass_indices):
    i, j = pass_indices
    print('Rises:', t[i].astimezone(brasil))
    print('Sets:', t[j].astimezone(brasil))

    # Set up the polar plot.
    ax = plt.subplot(111, projection='polar')
    ax.set_rlim([0, 90])
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Draw line and labels.
    θ = az.radians
    r = 90 - alt.degrees
    ax.plot(θ[i:j], r[i:j], 'ro--')
    for k in range(i, j):
        text = t[k].astimezone(brasil).strftime('%H:%M')
        ax.text(θ[k], r[k], text, ha='right', va='bottom')

plot_sky(passes[0])
