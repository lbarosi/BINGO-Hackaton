# Analysis of Supernova Dataset UNION2.1
# Created: Luciano Barosi
# 25.Ago.2019
# DATASET: Union2.1 from http://supernova.lbl.gov/
# Provides Class Supernova
# Ability to fetch and plot the data
# Fit different function and plot confidence curves.
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen  # That is an useful package
from scipy.constants import c  # speed of light
from scipy.optimize import curve_fit
from scipy.stats import chisquare, chi2
from scipy.integrate import quad

# Define nice figure size for MatplotLib
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 12
fig_size[1] = 6
plt.rcParams["figure.figsize"] = fig_size
#######################################################################################
class Supernova:
    """Supernova Data and Methods.
    Fetch, Plot and Fit data
    """

    def __init__(self):
        """Fetch SN data from given URL.
        Reorder data in ascending value of z ans store in
        np.arrays for use by the other methods.
        """
        SN_list = []
        z_array = np.array([])
        mod_array = np.array([])
        moderr_array = np.array([])
        f = urlopen("http://supernova.lbl.gov/Union/figures/SCPUnion2.1_mu_vs_z.txt")
        for line in f:
            pieces = line.decode("utf8").split("\n")
            # Header of data is commentd out, we do not need this
            # Data format is SN name, redshift, distance modulos, error
            # we read data from urlib.request line by line
            if "#" in pieces[0]:
                continue
            SN, z, mod, moderr, staterr = line.split()
            SN_list.append(SN)
            z_array = np.append(z_array, np.float64(z))
            mod_array = np.append(mod_array, np.float64(mod))
            moderr_array = np.append(moderr_array, np.float64(moderr))
        f.close()  # Always close you IO channels.
        dataRaw = np.vstack([z_array, mod_array, moderr_array]).T
        dataRaw = dataRaw[dataRaw[:, 0].argsort()]
        self.zz = dataRaw[:, 0]
        self.mu = dataRaw[:, 1]
        self.mu_err = dataRaw[:, 2]
        self.ZLIM = np.max(self.zz)
        return

    def distanceMPc(self):
        """"Calculate Luminosity distance from distance modules
        UNITs: MegaParsec
        """
        luminosityDistance = 0.00001 * 10 ** (self.mu / 5)
        distanceError = luminosityDistance * np.log(10) * self.mu_err
        return luminosityDistance, distanceError

    def dataToZ(self, *args):
        """"Filter data to z given in argument.
        If none is given, all data is returned.
        """
        if len(args) != 0:
            ZMAX = args[0]
            indx = np.where(self.zz < ZMAX)
            zfilter = self.zz[indx]
            mufilter = self.mu[indx]
            mufilterError = self.mu_err[indx]
            dist, distError = self.distanceMPc()
            dfilter = dist[indx]
            dfilterError = distError[indx]
        else:
            zfilter = self.zz
            mufilter = self.mu
            mufilterError = self.mu_err
            dist, distError = self.distanceMPc()
            dfilter = dist
            dfilterError = distError
        return zfilter, mufilter, mufilterError, dfilter, dfilterError

    def plotDataToZ(self, *args, **kwargs):
        """"Plot data Distance Modules x Z and Distance x z
        up to given z.
        z default to all data
        """
        if len(args) != 0:
            ZMAX = args[0]
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ(ZMAX)
        else:
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ()

        fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True)
        ax1.errorbar(
            zfilter,
            mufilter,
            yerr=mufilterError,
            fmt=".",
            capsize=0,
            elinewidth=1.0,
            ecolor=(0.6, 0.0, 1.0),
            color="green",
        )
        ax1.set_xlabel(r"$z$", fontsize=20)
        ax1.set_ylabel(r"$\mu$", fontsize=20)
        ax1.grid(b=True, which="both")
        ax1.set_title("Distance Modulus")
        ax2.errorbar(
            zfilter,
            dfilter,
            yerr=dfilterError,
            fmt=".",
            ecolor=(0.6, 0.0, 1.0),
            color="green",
            label="dataSN",
        )
        ax2.set_xlabel("redshift z")
        ax2.set_ylabel("Distance (Mpc)")
        ax2.set_ylim(bottom=0)
        ax2.grid(b=True, which="both")
        ax2.legend(loc="upper left")
        ax2.set_title("Luminosity Distance")
        return ax1, ax2

    def hubbleDiagram(self, *args):
        """"Plot Hubble diagram in terms of velocity and distance
        up to a given z.
        """
        if len(args) != 0:
            ZMAX = args[0]
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ(ZMAX)
        else:
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ()

        vel = c * zfilter / 1000  # velocity in km/s
        fig, ax = plt.subplots(constrained_layout=True)
        ax.errorbar(dfilter, vel, xerr=dfilterError, fmt=".")
        ax.set_xlabel("D(Mpc)")
        ax.set_ylabel("Velocity (Km/s)")
        ax.set_xlim(left=0)
        ax.grid(b=True, which="both")
        ax.set_title("Hubble relations, data from Supernova Cosmology Probe")
        sec = ax.secondary_yaxis(
            "right", functions=(lambda x: 1000 * x / c, lambda x: c * x / 1000)
        )
        sec.set_ylabel("z")
        return

    def dHubble(self, z, H0):
        return (1 / 1000) * c * z / H0

    def muHubble(self, z, H0):
        return 5 * np.log10(10 ** 6 * self.dHubble(z, H0)) - 5

    def dQ(self, z, H0, q):
        return (1 / 1000) * (c * z / H0) * (1 - (1 + q) * z / 2)

    def muQ(self, z, H0, q):
        return 5 * np.log10(10 ** 6 * self.dQ(z, H0, q)) - 5

    def dFRW(self, z, H0, OmM):
        def EE(z, H0, OmM):
            OmL = 1 - OmM
            return 1 / np.sqrt(OmM * (1 + z) ** 3 + OmL)

        tmp = quad(EE, 0, z, args=(H0, OmM))[0]
        dL = ((1 + z) * c / (1000 * H0)) * tmp
        return dL

    def muFRW(self, z, H0, OmM):
        DL = np.array([])
        for ZZ in z:
            tmp = self.dFRW(ZZ, H0, OmM)
            DL = np.append(DL, np.float64(tmp))
        return 5 * np.log10(10 ** 6 * DL) - 5

    def chiSq(self, x, y, err):
        return np.sum(((x - y) / err) ** 2)

    def fitDataMu(self, **kwargs):
        # parse arguments
        ZMAX = kwargs.get("ZMAX")
        FIT = kwargs.get("FIT")
        if ZMAX == None:
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ()
        else:
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ(ZMAX)
        fits = ("HUBBLE", "QUADRATIC")
        try:
            if FIT == "HUBBLE":
                func = self.muHubble
                INICIAL = 68
                BOUNDS = ([0], [100])
            elif FIT == "QUADRATIC":
                func = self.muQ
                INICIAL = (68, 0)
                BOUNDS = ([65, -5], [75, 5])
            elif FIT == "FRW":
                func = self.muFRW
                INICIAL = (68, 0.3)
                BOUNDS = ([65, 0], [75, 1])
            else:
                raise ValueError("Not a valid fit type: try HUBBLE or QUADRATIC")
        except ValueError as err:
            print(err.args)
        popt, pcov = curve_fit(
            func, zfilter, mufilter, sigma=mufilterError, p0=INICIAL, bounds=BOUNDS
        )
        perr = np.sqrt(np.diag(pcov))
        CHI2 = self.chiSq(mufilter, func(zfilter, *popt), mufilterError)
        dof = len(zfilter) - len(popt) - 1
        CHI2reduced = CHI2 / dof
        pvalue = chi2.sf(CHI2, dof)
        return popt, perr, CHI2reduced, pvalue

    def plotPvalues(self, **kwargs):
        zrange = np.linspace(0.1, np.max(self.zz), 20)
        pHubble = np.array([])
        pQuadratic = np.array([])
        pFRW = np.array([])
        for zm in zrange:
            pHubble = np.append(
                pHubble, np.float64(self.fitDataMu(FIT="HUBBLE", ZMAX=zm)[3])
            )
            pQuadratic = np.append(
                pQuadratic, np.float64(self.fitDataMu(FIT="QUADRATIC", ZMAX=zm)[3])
            )
            pFRW = np.append(pFRW, np.float64(self.fitDataMu(FIT="FRW", ZMAX=zm)[3]))

        fig, ax = plt.subplots(constrained_layout=True)
        ax.plot(zrange, pHubble, label="Hubble Law")
        ax.plot(zrange, pQuadratic, label="Deceleration Parameter")
        ax.plot(zrange, pFRW, label="Flat FRW")
        ax.set_xlim([0, np.max(self.zz)])
        ax.grid(b=True, which="both")
        ax.legend(loc="upper left")
        ax.set_title("p-value for different fitting functions")
        ax.set_xlabel("z")
        ax.set_ylabel("p-value")
        return ax

    def plotFitZ(self, *args):
        """" Plot data Distance Modules x Z and Fitted Curves
        ZMAX default to all values
        Argument should be a float or None.
        """
        # Filter data
        if len(args) != 0:
            ZMAX = args[0]
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ(ZMAX)
        else:
            zfilter, mufilter, mufilterError, dfilter, dfilterError = self.dataToZ()
            ZMAX = self.ZLIM
        # Fit the data
        HUBBLE = self.fitDataMu(FIT="HUBBLE", ZMAX=ZMAX)
        QUADRATIC = self.fitDataMu(FIT="QUADRATIC", ZMAX=ZMAX)
        FRW = self.fitDataMu(FIT="FRW", ZMAX=ZMAX)
        # Compute fitted values
        zrange = np.linspace(0.001, ZMAX, 200)
        fitHubbleMU = self.muHubble(zrange, *HUBBLE[0])
        fitQMU = self.muQ(zrange, *QUADRATIC[0])
        fitFRWMU = self.muFRW(zrange, *FRW[0])

        fig, ax = plt.subplots(constrained_layout=True)
        # Plot DATA with Errorbars
        ax.errorbar(
            zfilter,
            mufilter,
            yerr=mufilterError,
            fmt=".",
            capsize=0,
            elinewidth=1.0,
            ecolor=(0.6, 0.0, 1.0),
            color="green",
            label="SN UNION2.1 Data",
        )
        ax.set_xlabel(r"$z$", fontsize=20)
        ax.set_ylabel(r"$\mu$", fontsize=20)
        # Plot fitted functions
        ax.plot(zrange, fitHubbleMU, label="Hubble Law")
        ax.plot(zrange, fitQMU, label="Quadratic")
        ax.plot(zrange, fitFRWMU, label="Flat FRW")
        ax.grid(b=True, which="both")
        ax.legend(loc="lower right")
        ax.set_title("Supernova Data and Fits")
        return


if __name__ == "__main__":
    print("Executing as standalone script")
    SN = Supernova()
    SN.plotFitZ()
    SN.plotPvalues()
