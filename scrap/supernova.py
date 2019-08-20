import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen

SN_list = []
z_array = np.array([])
mod_array = np.array([])
moderr_array = np.array([])
f = urlopen('http://supernova.lbl.gov/Union/figures/SCPUnion2_mu_vs_z.txt')
for line in f:
    pieces = line.decode('utf8').split('\n')
    if '#' in pieces[0]: continue
    SN, z, mod, moderr = line.split()
    SN_list.append(SN)
    z_array = np.append(z_array,np.float64(z))
    mod_array = np.append(mod_array,np.float64(mod))
    moderr_array = np.append(moderr_array,np.float64(moderr))

f.close()
# %%
##############
##############
dz = 0.001
# distance in parsecs
dpc = 10.**(mod_array/5.+1.)
# and in megaparsecs (Mpc)
dMpc = dpc / 10.**6
# and the error on that distance:
dMe = 10.**((mod_array+moderr_array)/5.+1.-6.) - dMpc

# draw a linear-linear plot with all the data and the three Hubble relation curves:
plt.figure()
plt.errorbar(z_array,dMpc,xerr=dz,yerr=dMe,fmt='+')
plt.xlim([0,1.5])
plt.ylim([0,14000])
plt.xlabel('redshift z')
plt.ylabel('Luminosity distance (Mpc)')
plt.grid(b=True,which='both')
plt.title('Hubble relations, data from Supernova Cosmology Probe')
plt.show()

#numpy least square
A = np.vstack([dMpc, np.ones(len(dMpc))]).T
m, c = np.linalg.lstsq(A, z_array, rcond=None)[0]
m, c

#scipy linregress
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)


#scipy curve_fit
#https://micropore.wordpress.com/2017/02/04/python-fit-with-error-on-y-axis/
import numpy as np
from pylab import *
from scipy.optimize import curve_fit

def func(x, a, b, c):

return a * x *x + b*x + c

# test data and error
x = np.linspace(-10, 10, 100)
y0 = – 0.07 * x * x + 0.5 * x + 2.
noise = np.random.normal(0.0, 1.0, len(x))
y = y0 + noise

# curve fit [with only y-error]
popt, pcov = curve_fit(func, x, y, sigma=1./(noise*noise))
perr = np.sqrt(np.diag(pcov))

#print fit parameters and 1-sigma estimates
print(‘fit parameter 1-sigma error’)
print(‘———————————–‘)
for i in range(len(popt)):
print(str(popt[i])+’ +- ‘+str(perr[i]))

# prepare confidence level curves
nstd = 5. # to draw 5-sigma intervals
popt_up = popt + nstd * perr
popt_dw = popt – nstd * perr

fit = func(x, *popt)
fit_up = func(x, *popt_up)
fit_dw = func(x, *popt_dw)

#plot
fig, ax = plt.subplots(1)
rcParams[‘xtick.labelsize’] = 18
rcParams[‘ytick.labelsize’] = 18
rcParams[‘font.size’]= 20
errorbar(x, y0, yerr=noise, xerr=0, hold=True, ecolor=’k’, fmt=’none’, label=’data’)

xlabel(‘x’, fontsize=18)
ylabel(‘y’, fontsize=18)
title(‘fit with only Y-error’, fontsize=18)
plot(x, fit, ‘r’, lw=2, label=’best fit curve’)
plot(x, y0, ‘k–‘, lw=2, label=’True curve’)
ax.fill_between(x, fit_up, fit_dw, alpha=.25, label=’5-sigma interval’)
legend(loc=’lower right’,fontsize=18)
show()

#https://www.astroml.org/book_figures/chapter8/fig_huber_loss.html#book-fig-chapter8-fig-huber-loss

#https://towardsdatascience.com/from-scratch-bayesian-inference-markov-chain-monte-carlo-and-metropolis-hastings-in-python-ef21a29e25a
mod1=lambda t:np.random.normal(10,3,t)

#Form a population of 30,000 individual, with average=10 and scale=3
population = mod1(30000)
#Assume we are only able to observe 1,000 of these individuals.
observation = population[np.random.randint(0, 30000, 1000)]

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.hist( observation,bins=35 ,)
ax.set_xlabel("Value")
ax.set_ylabel("Frequency")
ax.set_title("Figure 1: Distribution of 1000 observations sampled from a population of 30,000 with mu=10, sigma=3")
mu_obs=observation.mean()
mu_obs

#The tranistion model defines how to move from sigma_current to sigma_new
transition_model = lambda x: [x[0],np.random.normal(x[1],0.5,(1,))]

def prior(x):
    #x[0] = mu, x[1]=sigma (new or current)
    #returns 1 for all valid values of sigma. Log(1) =0, so it does not affect the summation.
    #returns 0 for all invalid values of sigma (<=0). Log(0)=-infinity, and Log(negative number) is undefined.
    #It makes the new sigma infinitely unlikely.
    if(x[1] <=0):
        return 0
    return 1

#Computes the likelihood of the data given a sigma (new or current) according to equation (2)
def manual_log_like_normal(x,data):
    #x[0]=mu, x[1]=sigma (new or current)
    #data = the observation
    return np.sum(-np.log(x[1] * np.sqrt(2* np.pi) )-((data-x[0])**2) / (2*x[1]**2))

#Same as manual_log_like_normal(x,data), but using scipy implementation. It's pretty slow.
def log_lik_normal(x,data):
    #x[0]=mu, x[1]=sigma (new or current)
    #data = the observation
    return np.sum(np.log(scipy.stats.norm(x[0],x[1]).pdf(data)))


#Defines whether to accept or reject the new sample
def acceptance(x, x_new):
    if x_new>x:
        return True
    else:
        accept=np.random.uniform(0,1)
        # Since we did a log likelihood, we need to exponentiate in order to compare to the random number
        # less likely x_new are less likely to be accepted
        return (accept < (np.exp(x_new-x)))


def metropolis_hastings(likelihood_computer,prior, transition_model, param_init,iterations,data,acceptance_rule):
    # likelihood_computer(x,data): returns the likelihood that these parameters generated the data
    # transition_model(x): a function that draws a sample from a symmetric distribution and returns it
    # param_init: a starting sample
    # iterations: number of accepted to generated
    # data: the data that we wish to model
    # acceptance_rule(x,x_new): decides whether to accept or reject the new sample
    x = param_init
    accepted = []
    rejected = []
    for i in range(iterations):
        x_new =  transition_model(x)
        x_lik = likelihood_computer(x,data)
        x_new_lik = likelihood_computer(x_new,data)
        if (acceptance(x_lik + np.log(prior(x)),x_new_lik+np.log(prior(x_new)))):
            x = x_new
            accepted.append(x_new)
        else:
            rejected.append(x_new)

    return np.array(accepted), np.array(rejected)

accepted, rejected = metropolis_hastings(manual_log_like_normal,prior,transition_model,[mu_obs,0.1], 50000,observation,acceptance)




#https://github.com/fbeutler/Study-the-Universe-with-Python
