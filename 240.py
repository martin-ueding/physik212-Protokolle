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

import argparse
import matplotlib.pyplot as pl
import numpy as np
import scipy.optimize as op

__docformat__ = "restructuredtext en"

###############################################################################
#                                  Messwerte                                  #
###############################################################################

# Alle Werte sind in den SI-Standardeinheiten. Das Prefix ``a_`` steht für
# „Aufgabe a“.

# Messwerte für Spannung und Strom.
a_U_val = [1.78, 1.69, 1.5, 1.36, 1.19, .83, .7, .4, .21, .08]
a_I_val = [.085, .0805, .0715, .0655, .0565, .04, .034, .019, .01, .004]

# Deren Fehler.
a_U_err = 0.01
a_I_err = 0.001

# Vermessener Widerstand.
c_Rx_val = 22.0
c_Rx_err = 2.0

d_Rx_val = [0,    4,    8,    12,   16,   20,   24,   28,    32,    36]
d_U_val =  [.105, .373, .579, .722, .831, .915, .979, 1.031, 1.076, 1.114]
d_I_val =  [.1,   .082, .069, .053, .05,  .045, .04,  .036,  .034,  .031]

# Messfehler für Spannung und Strom.
d_U_err = 0.01
d_I_err = 0.001

# Anzahl Skalenteile.
f_l = 100.0

# Gesamtwiderstand des Helipots.
f_R_val = 5.3
f_R_err = 0.1

f_x_err = 0.1

# Skalenteile und Ausgangsspannung für Leerlauf.
f_x_0_val = np.array([10, 20, 30, 40, 50])
f_U1_0_val = np.array([.231, .445, .660, .875, 1.087])

# Skalenteile und Ausgangsspannung für Lastwiderstand von 20 Ω.
f_x_20_val = np.array([10, 20, 30, 40, 50])
f_U1_20_val = np.array([.228, .425, .613, .811, 1.011])

# Skalenteile und Ausgangsspannung für Lastwiderstand von 50 Ω.
f_x_50_val = np.array([10, 20, 30, 40, 50])
f_U1_50_val = np.array([.232, .440, .646, .851, 1.056])

# Fehler in der Spannungsmessung.
f_U_err = 0.001

h_x_val = 34.68
h_x_err = 0.1

h_U0_val = 1.0190
h_U0_err = 0.0005

# Gesamtwiderstand des Schleifendrahtpotentiometers.
i_R_val = 5.3
i_R_err = 0.0

# Anzahl der Skalenteile des Helipots, sowie die Gleichgewichtseinstellung.
i_l = 100
i_x_val = 53.45
i_x_err = 0.1

j_UM_val = 0.3
j_UM_err = 0.03

j_UD_val = 1.558
j_UD_err = 0.001

k_R0_val = 101.4
k_R0_err = 0.01

k_R_val = 5.3
k_R_err = 0.0

k_R1_val = 0.0
k_R1_err = 0.0

k_R2_val = 0.0
k_R2_err = 0.0

m_Platin_T_val = [22, 33, 45, 52, 62, 72, 82, 92, 100]
m_Platin_R_val = np.array([.109, .1226, .1226, .125, .129, .1316, .1353, .138, .1385]) * 1000

m_Manganin_T_val = [22, 39, 47, 55, 65, 75, 85, 95, 100]
m_Manganin_R_val = np.array([.576, .569, .573, .572, .568, .566, .568, .568, .568]) * 1000

m_Heissleiter_T_val = np.array([22, 43, 50, 60, 70, 80, 90, 100])
m_Heissleiter_R_val = np.array([8.48, 1.7, 1.52, .982, .817, .555, .426, .410]) * 1000

m_T_err = 2.0
m_R_err = 10.0

m_Heissleiter_R_err = 50.0

###############################################################################
#                                 Rechnungen                                  #
###############################################################################

plotargs = {
    #"color": "black",
    "linestyle": "None",
    #"markeredgecolor": "black",
    "markersize": 7
}

def main():
    options = _parse_args()

    aufgabe_a()
    aufgabe_b()
    aufgabe_e()
    aufgabe_f()
    aufgabe_g()
    aufgabe_h()
    aufgabe_l()
    aufgabe_n()

def aufgabe_a():
    print("Aufgabe a")

    I = np.array(a_I_val)
    U = np.array(a_U_val)

    ierr = np.ones(len(I)) * a_I_err
    uerr = np.ones(len(U)) * a_U_err

    def fit(I_val, RA_val):
        return I_val * RA_val

    popt, pconv = op.curve_fit(fit, I, U)

    global RA_val, RA_err
    RA_val = popt[0]
    RA_err = np.sqrt(pconv.diagonal()[0]**2 + RA_val + a_I_err)

    x = np.linspace(min(I), max(I), 100)
    y = fit(x, *popt)

    print "R_A = {val} ± {err} Ω".format(val=RA_val, err=RA_err)

    pl.errorbar(I, U, yerr=uerr, xerr=ierr, **plotargs)
    pl.grid(True)
    pl.plot(x, y, color="black")
    pl.title(ur"$U$-$I$-Abhängigkeit")
    pl.ylabel(ur"$U$ / [V]")
    pl.xlabel(ur"$I$ / [A]")

    pl.savefig("A.pdf")

    pl.clf()

def aufgabe_b():
    print("Aufgabe b")

    # TODO Implementieren

def aufgabe_e():
    print("Aufgabe e")

    I = np.array(d_I_val)
    U = np.array(d_U_val)

    ierr = np.ones(len(I)) * d_I_err
    uerr = np.ones(len(U)) * d_U_err

    def fit(I_val, U0s_val, Ris_val):
        return U0s_val - I_val * Ris_val

    popt, pconv = op.curve_fit(fit, I, U)

    global RA_val, RA_err
    U0s_val, Ris_val = popt
    U0s_err, Ris_err = pconv.diagonal()

    U0s_err = np.sqrt(U0s_err**2 + d_U_err**2)
    Ris_err = np.sqrt(Ris_err**2 + (Ris_val * d_I_err)**2)

    print "U_0^s = {val} ± {err} V".format(val=U0s_val, err=U0s_err)
    print "R_i^s = {val} ± {err} Ω".format(val=Ris_val, err=Ris_err)

    x = np.linspace(min(I), max(I), 100)
    y = fit(x, *popt)

    pl.errorbar(I, U, yerr=uerr, xerr=ierr, **plotargs)
    pl.title(ur"$U_1$-$I$-Abhängigkeit")
    pl.grid(True)
    pl.plot(x, y, color="black")
    pl.ylabel(ur"$U$ / [V]")
    pl.xlabel(ur"$I$ / [A]")

    pl.savefig("e.pdf")

    pl.clf()

def aufgabe_f():
    print("Aufgabe f")

    x1 = np.array(f_x_0_val)
    y1 = np.array(f_U1_0_val)

    x2 = np.array(f_x_20_val)
    y2 = np.array(f_U1_20_val)

    x3 = np.array(f_x_50_val)
    y3 = np.array(f_U1_50_val)

    errx = np.ones(len(x1)) * f_x_err
    erry = np.ones(len(y1)) * f_U_err

    pl.errorbar(x1, y1, xerr=errx, yerr=erry, label=ur"Leerlauf", marker="+", **plotargs)
    pl.errorbar(x3, y3, xerr=errx, yerr=erry, label=ur"$50 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.errorbar(x2, y2, xerr=errx, yerr=erry, label=ur"$20 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.grid(True)
    pl.legend(loc="best")
    pl.title(ur"$U$-$x$-Abhängigkeit")
    pl.xlabel(ur"$x$")
    pl.ylabel(ur"$U$ / [V]")

    pl.savefig("f.pdf")

    pl.clf()

def aufgabe_g():
    print("Aufgabe g")

    x1 = f_x_0_val
    y1 = f_U1_0_val**2 / f_R_val

    y1_err = np.sqrt(
        (2 * f_U1_0_val / f_R_val * f_U_err)**2
        + (f_U1_0_val**2 / f_R_val**2 * f_R_err)**2
    )

    x2 = f_x_20_val
    y2 = f_U1_20_val**2 / f_R_val

    y2_err = np.sqrt(
        (2 * f_U1_20_val / f_R_val * f_U_err)**2
        + (f_U1_20_val**2 / f_R_val**2 * f_R_err)**2
    )

    x3 = f_x_50_val
    y3 = f_U1_50_val**2 / f_R_val

    y3_err = np.sqrt(
        (2 * f_U1_50_val / f_R_val * f_U_err)**2
        + (f_U1_50_val**2 / f_R_val**2 * f_R_err)**2
    )

    errx = np.ones(len(x1)) * f_x_err

    pl.grid(True)
    pl.errorbar(x1, y1, xerr=errx, yerr=y1_err, label=ur"Leerlauf", marker="+", **plotargs)
    pl.errorbar(x3, y3, xerr=errx, yerr=y2_err, label=ur"$50 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.errorbar(x2, y2, xerr=errx, yerr=y3_err, label=ur"$20 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.title(ur"$P$-$x$-Abhängigkeit")
    pl.xlabel(ur"$x$")
    pl.ylabel(ur"$P$ / [W]")
    pl.legend(loc="best")

    pl.savefig("g.pdf")

    pl.clf()

def aufgabe_h():
    print "Aufgabe h"

    # Berechne Spannung des Netzgeräts.
    U = h_U0_val * i_l / h_x_val
    U_err = np.sqrt(
        (i_l / h_x_val * h_U0_err)**2
        + (h_U0_val * i_l / (h_x_val**2) * h_x_err)**2
    )

    print "Spannung Netzgerät", U, "±", U_err, "V"

    # Berechne die Spannung der Batterie.
    UB = U * i_x_val / i_l
    UB_err = np.sqrt(
        (i_x_val / i_l * U_err)**2
        + (U / i_l * i_x_err)**2
    )

    print "Spannung Batterie", UB, "±", UB_err, "V"

def aufgabe_l():
    print("Aufgabe l")

    U = 3
    U_max = 0.04
    R_innen = 100

    I_max = U_max / R_innen

    print("Maximaler Strom für das Galvanometer:", I_max)

def aufgabe_n():
    print("Aufgabe n")

    x1 = np.array(m_Platin_T_val)
    x1_err = np.ones(x1.shape) * m_T_err
    y1 = m_Platin_R_val
    y1_err = np.ones(y1.shape) * m_R_err

    x2 = np.array(m_Manganin_T_val)
    x2_err = np.ones(x2.shape) * m_T_err
    y2 = m_Manganin_R_val
    y2_err = np.ones(y2.shape) * m_R_err

    def R(T, R0, alpha):
        return R0 * (1 - alpha * T)

    popt, pconv = op.curve_fit(R, x1, y1)

    R01, alpha1 = popt
    R01_err, alpha1_err = pconv.diagonal()

    x = np.linspace(min(x2), max(x2), 100)
    y = R(x, *popt)
    pl.plot(x, y, label="Fit Platin", color="black")

    popt, pconv = op.curve_fit(R, x2, y2)

    R02, alpha2 = popt
    R02_err, alpha2_err = pconv.diagonal()

    x = np.linspace(min(x2), max(x2), 100)
    y = R(x, *popt)
    pl.plot(x, y, label="Fit Manganin", color="black", linestyle="--")

    pl.errorbar(x1, y1, xerr=x1_err, yerr=y1_err, label="Platin", marker="+", **plotargs)
    pl.errorbar(x2, y2, xerr=x2_err, yerr=y2_err, label="Manganin", marker="+", **plotargs)
    pl.title(ur"$R$-$\theta$-Abhängigkeit")
    pl.xlabel(ur"$\theta / ^\circ \mathrm{C}$")
    pl.ylabel(ur"$R$")

    pl.grid(True)
    pl.legend(loc="best")

    pl.savefig("Metall.pdf")

    pl.clf()

    # Heißleiter

    x = 1/(m_Heissleiter_T_val + 273.15)
    y = np.log(m_Heissleiter_R_val)

    x_err = np.abs(x**2 * m_T_err)
    y_err = np.abs(1/m_Heissleiter_R_val * m_Heissleiter_R_err)

    k = 1.3806488e-23

    def RH(T, a, b):
        return a * T + b

    popt, pconv = op.curve_fit(RH, x, y, sigma=y_err)

    fit_x = np.linspace(min(x), max(x), 100)
    fit_y = RH(fit_x, *popt)
    pl.plot(fit_x, fit_y, label=u"Fit Heißleiter", color="black", linestyle="--")

    pl.errorbar(x, y, xerr=x_err, yerr=y_err, label=u"Heißleiter", marker="+", **plotargs)
    pl.title(ur"$R$-$T$-Abhängigkeit")
    pl.xlabel(ur"$1/T \, / \, 1/ \mathrm{K}$")
    pl.ylabel(ur"$\ln\left(R / \mathrm{\Omega}\right)$")

    pl.grid(True)
    pl.legend(loc="best")

    pl.savefig("Heissleiter.pdf")

    pl.clf()

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    #parser.add_argument("args", metavar="N", type=str, nargs="*", help="Positional arguments.")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()

if __name__ == "__main__":
    main()
