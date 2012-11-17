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

# Vorwiderstand im Voltmeter.
a_Vorwiderstand_val = 0.0
a_Vorwiderstand_err = 0.0

# Shunt im Ampèremeter.
a_Shunt_val = 0.0
a_Shunt_err = 0.0

# Vermessener Widerstand.
c_Rx_val = 22.0
c_Rx_err = 2.0

d_Rx_val = [0,    4,    8,    12,   16,   20,   24,   28,    32,    36]
d_U_val =  [.105, .373, .579, .722, .831, .915, .979, 1.031, 1.076, 1.114]
d_I_val =  [.1,   .082, .069, .053, .05,  .045, .04,  .036,  .034,  .031]

# Messfehler für Spannung und Strom.
d_U_err = 0.001
d_I_err = 0.001

# Anzahl Skalenteile.
f_l = 100.0

# Gesamtwiderstand des Helipots.
f_R_val = 5.3
f_R_err = 0.1

# Skalenteile und Ausgangsspannung für Leerlauf.
f_x_0_val = [10, 20, 30, 40, 50]
f_U1_0_val = [.231, .445, .660, .875, 1.087]

# Skalenteile und Ausgangsspannung für Lastwiderstand von 20 Ω.
f_x_20_val = [10, 20, 30, 40, 50]
f_U1_20_val = [.228, .425, .613, .811, 1.011]

# Skalenteile und Ausgangsspannung für Lastwiderstand von 50 Ω.
f_x_50_val = [10, 20, 30, 40, 50]
f_U1_50_val = [.232, .440, .646, .851, 1.056]

# Fehler in der Spannungsmessung.
f_U_err = 0.3

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
m_Platin_R_val = np.array([.109, .1226, .1226, .125, .129, .1316, .1353, .138, .1385])

m_Manganin_T_val = [22, 39, 47, 55, 65, 75, 85, 95, 100]
m_Manganin_R_val = np.array([.576, .569, .573, .572, .568, .566, .568, .568, .568])

m_Heissleiter_T_val = [22, 43, 50, 60, 70, 80, 90, 100]
m_Heissleiter_R_val = np.array([8.48, 1.7, 1.52, .982, .817, .555, .426, .410]) * 1000

m_T_err = 2.0
m_R_err = 10.0

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
    aufgabe_n()

def aufgabe_a():
    U = np.array(a_U_val)
    I = np.array(a_I_val)

    uerr = np.ones(len(U)) * a_U_err
    ierr = np.ones(len(I)) * a_I_err

    def fit(I_val, RA_val):
        return I_val * RA_val

    popt, pconv = op.curve_fit(fit, I, U)

    global RA_val, RA_err
    RA_val = popt[0]
    RA_err = pconv.diagonal()[0]

    x = np.linspace(min(I), max(I), 100)
    y = fit(x, *popt)

    print "R_A = {val} ± {err} Ω".format(val=RA_val, err=RA_err)

    pl.errorbar(I, U, xerr=ierr, yerr=uerr, **plotargs)
    pl.grid(True)
    pl.plot(x, y, color="black")
    pl.title(ur"$U$-$I$-Abhängigkeit")
    pl.xlabel(ur"$U$ / [V]")
    pl.ylabel(ur"$I$ / [A]")

    pl.savefig("A.pdf")

    pl.clf()

def aufgabe_b():
    # TODO Implementieren
    pass

def aufgabe_e():
    U = np.array(d_U_val)
    I = np.array(d_I_val)

    uerr = np.ones(len(U)) * d_U_err
    ierr = np.ones(len(I)) * d_I_err

    def fit(I_val, U0s_val, Ris_val):
        return U0s_val + I_val * Ris_val

    popt, pconv = op.curve_fit(fit, I, U)

    global RA_val, RA_err
    U0s_val, Ris_val = popt
    U0s_err, Ris_err = pconv.diagonal()

    print "U_0^s = {val} ± {err} V".format(val=U0s_val, err=U0s_err)
    print "R_i^s = {val} ± {err} Ω".format(val=Ris_val, err=Ris_err)

    x = np.linspace(min(I), max(I), 100)
    y = fit(x, *popt)

    pl.errorbar(I, U, xerr=ierr, yerr=uerr, **plotargs)
    pl.title(ur"$U_1$-$I$-Abhängigkeit")
    pl.grid(True)
    pl.plot(x, y, color="black")
    pl.xlabel(ur"$U$ / [V]")
    pl.ylabel(ur"$I$ / [A]")

    pl.savefig("e.pdf")

    pl.clf()

def aufgabe_f():
    x1 = np.array(f_x_0_val)
    y1 = np.array(f_U1_0_val)

    x2 = np.array(f_x_20_val)
    y2 = np.array(f_U1_20_val)

    x3 = np.array(f_x_50_val)
    y3 = np.array(f_U1_50_val)

    err1 = np.ones(len(x1)) * f_U_err
    err2 = np.ones(len(x2)) * f_U_err
    err3 = np.ones(len(x3)) * f_U_err

    pl.errorbar(x1, y1, yerr=err1, label=ur"Leerlauf", marker="+", **plotargs)
    pl.errorbar(x2, y2, yerr=err2, label=ur"$20 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.errorbar(x3, y3, yerr=err3, label=ur"$50 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.grid(True)
    pl.legend()
    pl.title(ur"$U$-$x$-Abhängigkeit")
    pl.xlabel(ur"$x$")
    pl.ylabel(ur"$U$ / [V]")

    pl.savefig("f.pdf")

    pl.clf()

def aufgabe_g():
    x1 = np.array(f_x_0_val)
    y1 = np.array(f_U1_0_val)**2 / f_R_val

    x2 = np.array(f_x_20_val)
    y2 = np.array(f_U1_20_val)**2 / f_R_val

    x3 = np.array(f_x_50_val)
    y3 = np.array(f_U1_50_val)**2 / f_R_val

    pl.grid(True)
    pl.plot(x1, y1, label=ur"Leerlauf", marker="+", **plotargs)
    pl.plot(x2, y2, label=ur"$20 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.plot(x3, y3, label=ur"$50 \, \mathrm{\Omega}$", marker="+", **plotargs)
    pl.title(ur"$P$-$x$-Abhängigkeit")
    pl.xlabel(ur"$x$")
    pl.ylabel(ur"$P$ / [W]")
    pl.legend()

    pl.savefig("g.pdf")

    pl.clf()

def aufgabe_n():
    x1 = np.array(m_Platin_T_val)
    y1 = m_Platin_R_val

    x2 = np.array(m_Manganin_T_val)
    y2 = m_Manganin_R_val

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

    pl.plot(x1, y1, label="Platin", marker="+", **plotargs)
    pl.plot(x2, y2, label="Manganin", marker="+", **plotargs)
    pl.title(ur"$R$-$\theta$-Abhängigkeit")
    pl.xlabel(ur"$\theta$")
    pl.ylabel(ur"$R$")

    pl.grid(True)
    pl.legend(loc="right")

    pl.savefig("Metall.pdf")

    pl.clf()

    # Heißleiter

    x = np.array(m_Heissleiter_T_val)
    y = m_Heissleiter_R_val

    pl.plot(x, y, label=u"Heißleiter", marker="+", **plotargs)
    pl.title(ur"$R$-$\theta$-Abhängigkeit")
    pl.xlabel(ur"$\theta$")
    pl.ylabel(ur"$R$")

    pl.grid(True)
    pl.legend()

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
