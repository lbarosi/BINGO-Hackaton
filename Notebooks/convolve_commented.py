import numpy as np
from matplotlib import pyplot as plt
### NOTE: This is not being used
### But you may try to use this to prove convolution theorem
### prepare your way for problems
from scipy.signal import fftconvolve

#------------------------------------------------------------
# Generate random x, y with a given covariance length
np.random.seed(1)
### this is not a power of 2 and you are not taking care of this
### you should have inprecision in frequencies and boundary effects
x = np.linspace(0, 1, 500)
### that's just cumbersome
h = 0.01
C = np.exp(-0.5 * (x - x[:, None]) ** 2 / h ** 2)
y = 0.8 + 0.3 * np.random.multivariate_normal(np.zeros(len(x)), C)

#------------------------------------------------------------
# Define a normalized top-hat window function
### This is not normalized, the code does this afterwards.
### There is no reason to define tophat in terms of x this way
### you are positioning a 80 cols tophat in a fixed position of your signal
### this is not the same as convolving the signal
w = np.zeros_like(x)
w[(x > 0.12) & (x < 0.28)] = 1

#------------------------------------------------------------
# Perform the convolution
### this is thw window in the x with length 500 then you chopp the
### the indices that are unacessible by the window.
### you could just have started with your y signal correct
### full mode includes boundary effects
y_norm = np.convolve(np.ones_like(y), w, mode='full')
valid_indices = (y_norm != 0)
y_norm = y_norm[valid_indices]
### this one is fine
y_w = np.convolve(y, w, mode='full')[valid_indices] / y_norm

# trick: convolve with x-coordinate to find the center of the window at
#        each point.
### alas this was the only one in this code.
x_w = np.convolve(x, w, mode='full')[valid_indices] / y_norm

#------------------------------------------------------------
# Compute the Fourier transforms of the signal and window
### this is just personal preference, I rather use scipy.fftpack.fft
y_fft = np.fft.fft(y)
w_fft = np.fft.fft(w)

yw_fft = y_fft * w_fft
### There is not a plot for this, guess why?
### Convolution theorem says this is equals to y_w
yw_final = np.fft.ifft(yw_fft)

# FFT k modes
### Well, this means -N/2 + N = N/2
### This seems a hard way to obtain a simple result.
N = len(x)
k = - 0.5 * N + np.arange(N) * 1. / N / (x[1] - x[0])
#------------------------------------------------------------
# Set up the plots
### The plots were changed to shorten the code.
fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize=(10, 10))

ax[0,0].plot(x, y, '-k', label=r'data $D(x)$')
ax[0,0].legend()
ax[0,0].xaxis.set_major_formatter(plt.NullFormatter())
ax[0,0].set_ylabel('$D$')
ax[0,0].set_xlim(0.01, 0.99)
ax[0,0].set_ylim(0, 2.0)

#----------------------------------------
# plot the convolution
ax[0,1].plot(x_w, y_w, '-k')
ax[0,1].set_xlabel('$x$')
ax[0,1].set_ylabel('$D_W$')
ax[0,1].set_xlim(0.01, 0.99)
ax[0,1].set_ylim(0, 1.99)

#----------------------------------------
# plot the Fourier transforms
ax[1,0].plot(k, abs(np.fft.fftshift(y_fft)), '-k', color = "blue")
ax[1,0].set_xlim(-100, 100)
ax[1,0].set_ylim(-5, 85)

ax[1,0].plot(k, abs(np.fft.fftshift(w_fft)), '-k', color = "red")
ax[1,0].set_xlim(-100, 100)
ax[1,0].set_ylim(-5, 85)

#----------------------------------------
# plot the product of Fourier transforms
ax[1,1].plot(k, abs(np.fft.fftshift(yw_fft)), '-k')
ax[1,1].set_xlim(-100, 100)
ax[1,1].set_ylim(-100, 3500)
ax[1,1].set_xlabel('$k$')

plt.show()

### I told you!
### Get the x-axis right!
### Get the padding right!
### Boundaries!
fig = plt.figure()
plt.plot(y_w, color = "blue", label = "convolution")
plt.plot(np.abs(yw_final)/80, color = "red", label = "inverse FFT")
plt.show()
