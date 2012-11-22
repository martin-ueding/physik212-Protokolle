#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

import matplotlib.pyplot as pl
import numpy as np
import scipy.optimize as op

__docformat__ = "restructuredtext en"

###############################################################################
#                                  Messwerte                                  #
###############################################################################

# Kapazitätsmessung

a_C0_val = 20e-6
a_C0_err = 0.0

a_x_val = 980.0
a_x_err = 5.0

a_l_val = 1000.0

# Impedanzmessung

b_l_val = 1000.0
b_x_val = 77.0
b_x_err = 5.0

b_L0_val = 226.0
b_L0_err = 0.0

# Strom- und Spannungsmessung

c_R_val = 100.0
c_R_err = 0.1

c_omega_val = 2e3 * 2 * np.pi
c_omega_err = 0.0

c_U_val = 0.3933
c_U_err = 0.0001

c_I_val = 11.326e-3
c_I_err = 0.001e-3

# Phasenschieber

d_l_val = 1000.0

d_R_val = 100.0

d_C_val = 20.0

d_x_val = np.array([0, 20, 50, 70, 90, 110, 150, 330, 870, 1000, np.inf])
d_UR_val = np.array([404.4, 400.0, 348.8, 308.0, 270.5, 237.8, 188.1, 92.3,
                     45.5, 29.9, 0.0]) * 1e-3
d_UC_val = np.array([1.8, 24.6, 155.3, 216.7, 259.9, 290.5, 328.5, 379.4,
                     394.4, 398.5, 404.9]) * 1e-3

d_x_err = 20
d_U_err = 0.5e-3

# Filter

e_R = 100.0
e_C = 1.5e-6

e_nu_tief = np.array([200, 275, 380, 525, 724, 1000, 1379, 1903, 2626, 3623,
                      5000]) * 2 * np.pi
e_UA_tief = np.array([144.4, 108.0, 79.1, 57.4, 41.2, 29.4, 20.7, 14.8, 10.5,
                      7.3, 4.0]) * 1e-3

e_nu_hoch = e_nu_tief
e_UA_hoch = np.array([373.0, 385.6, 393.0, 397.1, 399.3, 400.6, 401.7, 402.6,
                      403.4, 404.4, 405.6]) * 1e-3

e_nu_sperr = np.array([200, 275, 380, 525, 724, 1000, 1379, 1903, 2626, 3623,
                      5000, 675.0]) * 2 * np.pi
e_UA_sperr = np.array([395.0, 383.3, 350.4, 237.1, 84.3, 304.6, 370.0, 391.6,
                       400.6, 405.5, 408.6, 35.4]) * 1e-3

e_UA_err = 0.2e-3

e_UE_val = 403.9e-3

# Schwingkreis

i_C = 1.5e-6

i_nu_val = np.array([ 1, 10, 50, 100, 200, 300, 400, 450, 500, 530, 560, 590,
                     620, 640, 650, 655, 658, 662, 665, 668, 670, 672, 674,
                     675, 676, 678, 683, 690, 700, 710, 720, 730, 770, 820,
                     880, 960, 1100, 1400, 1700, 2000 ])

i_UE_val = np.array([104.0e-3, 383.0e-3, 402.0e-3, 403.6e-3, 404.4e-3,
                     404.7e-3, 404.7e-3, 404.7e-3, 404.7e-3, 404.4e-3,
                     404.0e-3, 402.6e-3, 399.7e-3, 393.3e-3, 386.7e-3,
                     381.9e-3, 378.6e-3, 373.9e-3, 370.2e-3, 367.0e-3,
                     365.1e-3, 363.7e-3, 362.8e-3, 362.5e-3, 362.4e-3,
                     632.7e-3, 365.5e-3, 372.5e-3, 382.0e-3, 389.1e-3,
                     393.5e-3, 396.3e-3, 400.3e-3, 402.8e-3, 403.8e-3,
                     404.4e-3, 404.8e-3, 405.2e-3, 405.6e-3, 405.9e-3])

i_UC_val = np.array([104.0e-3, 384.0e-3, 404.0e-3, 413.2e-3, 444.5e-3,
                     506.0e-3, 626.1e-3, 730.8e-3, 897.0e-3, 1051.7e-3,
                     1284.3e-3, 1668.3e-3, 2396.3e-3, 3323.7e-3, 4.039, 4.443,
                     4.698, 5.022, 5.245, 5.427, 5.515, 5.571, 5.594, 5.591,
                     5.580, 5.531, 5.272, 4.705, 3.837, 3.1179, 2.5864, 2.1880,
                     1.3097, 0.845, 0.5790, 0.3973, 0.2455, 0.1224, 0.0747,
                     0.0506])

i_U_err = np.array([3.0e-3, 3.0e-3, 3.0e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3,
                    0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3,
                    0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3,
                    0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3,
                    0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3,
                    0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3, 0.5e-3])

###############################################################################
#                                 Rechnungen                                  #
###############################################################################

plotargs = {
    #"color": "black",
    "linestyle": "None",
    #"markeredgecolor": "black",
    #"markersize": 7
}

def main():
    aufgabe_a()
    print
    aufgabe_b()
    print
    aufgabe_d()
    print
    aufgabe_e()
    print
    aufgabe_i()

def aufgabe_a():
    print "Aufgabe a"

    Cx_val = a_x_val / a_l_val * a_C0_val
    Cx_err = np.sqrt(
        (a_x_val / a_l_val * a_C0_err)**2
        + (1 / a_l_val * a_C0_val * a_x_err)**2
    )

    print "C_x = {val} ± {err} F".format(val=Cx_val, err=Cx_err)

def aufgabe_b():
    print "Aufgabe b"

    Lx_val = b_x_val / b_l_val * b_L0_val
    Lx_err = np.sqrt(
        (b_x_val / b_l_val * b_L0_err)**2
        + (1 / b_l_val * b_L0_val * b_x_err)**2
    )

    print "L_x = {val} ± {err} H".format(val=Lx_val, err=Lx_err)

def aufgabe_d():
    print "Aufgabe d"

    with open("d_zeiger.tex", "w") as f:
        f.write(r"\begin{tikzpicture}[scale=30]")

        for UC, UR in zip(d_UC_val, d_UR_val):
            a = np.arctan2(UC, UR) * 180 / np.pi
            f.write(r"\draw[->] (0, 0) -- ++({a}:{UR});".format(a=a, UR=UR))
            f.write(r"\draw[->] ({a}:{UR}) -- ++({b}:{UC});".format(a=a, UR=UR, b=a-90, UC=UC))

        f.write(r"\end{tikzpicture}")

def aufgabe_e():
    print "Aufgabe e"

    nu_gr = 1 / (e_R * e_C * 2 * np.pi)

    x_tief = e_nu_tief / nu_gr
    y_tief = e_UA_tief / e_UE_val
    db_tief = 10.0 * np.log(y_tief) / np.log(10)

    x_hoch = e_nu_hoch / nu_gr
    y_hoch = e_UA_hoch / e_UE_val
    db_hoch = 10.0 * np.log(y_hoch) / np.log(10)

    x_sperr = e_nu_sperr / (675.0 * 2 * np.pi)
    y_sperr = e_UA_sperr / e_UE_val
    db_sperr = 10.0 * np.log(y_sperr) / np.log(10)

    print x_tief
    print y_tief

    pl.clf()
    pl.loglog(x_tief, y_tief, marker="o", label="Tiefpass", **plotargs)
    ax1 = pl.subplot(111)
    ax2 = pl.twinx()
    pl.plot(x_tief, db_tief, **plotargs)
    pl.title("Tiefpass")
    pl.legend(loc="best")
    ax1.grid(True)
    ax1.set_ylabel(ur"Übertragungsfunktion")
    ax1.set_xlabel(ur"$\nu / \nu_\mathrm{gr}$")
    ax2.set_ylabel(ur"Übertragung in dB")
    ax1.set_ylim(np.min(y_tief), 1)
    ax2.set_ylim(np.min(db_tief), 0)
    pl.savefig("e_tief.pdf")

    pl.clf()
    pl.loglog(x_hoch, y_hoch, marker="o", label="Hochpass", **plotargs)
    ax1 = pl.subplot(111)
    ax2 = pl.twinx()
    pl.plot(x_hoch, db_hoch, **plotargs)
    pl.title("Hochpass")
    pl.legend(loc="best")
    pl.xlabel(ur"$\nu / \nu_\mathrm{gr}$")
    ax2.grid(True)
    ax1.set_ylabel(ur"Übertragungsfunktion")
    ax1.set_xlabel(ur"$\nu / \nu_\mathrm{gr}$")
    ax2.set_ylabel(ur"Übertragung in dB")
    ax1.set_ylim(np.min(y_hoch), np.max(y_hoch))
    ax2.set_ylim(np.min(db_hoch), np.max(db_hoch))
    pl.savefig("e_hoch.pdf")

    pl.clf()
    pl.loglog(x_sperr, y_sperr, marker="o", label="Sperrfilter", **plotargs)
    ax1 = pl.subplot(111)
    ax2 = pl.twinx()
    pl.plot(x_sperr, db_sperr, **plotargs)
    pl.title("Sperrfilter")
    pl.legend(loc="best")
    pl.xlabel(ur"$\nu / \nu_\mathrm{gr}$")
    ax1.grid(True)
    ax1.set_ylabel(ur"Übertragungsfunktion")
    ax1.set_xlabel(ur"$\nu / \nu_\mathrm{gr}$")
    ax2.set_ylabel(ur"Übertragung in dB")
    ax1.set_ylim(np.min(y_sperr), np.max(y_sperr))
    ax2.set_ylim(np.min(db_sperr), np.max(db_sperr))
    pl.savefig("e_sperr.pdf")

def aufgabe_i():
    print "Aufgabe i"

    x = i_nu_val
    y = i_UC_val / i_UE_val
    y_err = np.sqrt(
        (1 / i_UE_val * i_U_err)**2
        +(i_UC_val / (i_UE_val**2) * i_U_err)**2
    )

    def resonanz(omega, omega0, mu, Q):
        return mu / np.sqrt((omega - omega0)**2 + omega**2 * omega0**2 / Q**2)

    popt, pconv = op.curve_fit(resonanz, x, y, p0=[675.0 * 2 * np.pi, 1, 1000], sigma=1/y_err)

    omega0 = popt[0]
    omega0_err = np.diag(pconv)[0]

    mu = popt[1]
    mu_err = np.diag(pconv)[1]

    Q = popt[2]
    Q_err = np.diag(pconv)[2]

    print "f₀ = {0} ± {1} Hz".format(omega0, omega0_err)
    print "μ = {0} ± {1}".format(mu, mu_err)
    print "Q = {0} ± {1}".format(Q, Q_err)

    plot_x = np.linspace(min(x), max(x), 1000)
    plot_y = resonanz(plot_x, *popt)

    pl.clf()
    pl.plot(plot_x, plot_y, label="Fit")
    pl.errorbar(x, y, yerr=y_err, marker="+", label="Messdaten", **plotargs)
    pl.legend(loc="best")
    pl.xlabel(ur"$\nu \, / \, \mathrm{Hz}$")
    pl.ylabel(ur"")
    pl.grid(True)

    pl.savefig("i.pdf")

if __name__ == "__main__":
    main()
