#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

import matplotlib.pyplot as pl
import numpy as np

I_err = 0.1
P_err = 1.0
R_err = 0.05
U_err = 0.5

plotargs = {
    #"color": "black",
    "linestyle": "None",
    #"markeredgecolor": "black",
    #"markersize": 4
}

__docformat__ = "restructuredtext en"

def a():
    ###########################################################################
    #                                Messwerte                                #
    ###########################################################################

    with open("Ueding-Vorversuch-2.txt") as f:
        d = np.genfromtxt(f, names=["I_1", "U_1", "cos_1", "I_2", "U_2", "cos_2", "P_1", "P_2"])

    I = d["I_2"]
    P_W = d["P_2"]
    U_R = np.array([
        42.5,
        41.43,
        41.08,
        40.03,
        38.79,
        37.63,
        35.87,
        34.06,
        31.71,
        29.35,
    ])
    U = d["U_2"]
    R = U_R / I

    R_err = np.sqrt(
        (1/I * U_err)**2
        + (U_R / (I**2) * I_err)**2
    )

    ###########################################################################
    #                               Rechnungen                                #
    ###########################################################################

    P_S = I * U
    cos = U_R / U

    pl.clf()
    pl.grid(True)
    pl.errorbar(R, P_S, label=ur"$P_S$", xerr=R_err, yerr=np.ones(P_S.size) * P_err, **plotargs)
    pl.errorbar(R, P_W, label=ur"$P_W$", xerr=R_err, yerr=np.ones(P_W.size) * P_err, **plotargs)
    pl.errorbar(R, P_S * cos, label=ur"$P_S \cos(\phi)$", xerr=R_err, yerr=np.ones(P_W.size) * P_err, **plotargs)
    pl.title(u"Leistungen gegen Widerstand")
    pl.xlabel(ur"$R / \mathrm{\Omega}$")
    pl.ylabel(ur"$P / \mathrm{W}$")
    pl.legend()
    pl.savefig("b.pdf")

def c():
    ###########################################################################
    #                                Messwerte                                #
    ###########################################################################

    with open("Ueding-Versuch-1.txt") as f:
        d = np.genfromtxt(f, names=["I_1", "U_1", "cos_1", "I_2", "U_2", "cos_2", "P_1", "P_2"])

    I_2 = d["I_2"]
    I_1 = d["I_1"]
    U_2 = d["U_2"]
    U_1 = d["U_1"]
    P_W1 = d["P_1"]
    P_W2 = d["P_2"]
    cos_1 = d["cos_1"]
    cos_2 = d["cos_2"]

    R_1 = R_2 = 0.5

    I_2_err = np.ones(I_2.shape) * I_err

    ###########################################################################
    #                               Rechnungen                                #
    ###########################################################################

    P_W1_err = np.ones(P_W1.shape) * P_err

    P_S2 = U_2 * I_2
    P_S2_err = np.sqrt(
        (I_2 * U_err)**2
        + (U_2 * I_err)**2
    )
    print "P_S2"
    print np.array([P_S2, P_S2_err]).transpose()
    print

    P_Cu = R_1 * I_1**2 + R_2 * I_2**2
    P_Cu_err = np.sqrt(
        (2 * R_1 * I_1 * I_err)**2
        + (I_1**2 * R_err)**2
        + (2 * R_2 * I_1 * I_err)**2
        + (I_2**2 * R_err)**2
    )
    print "P_Cu"
    print np.array([P_Cu, P_Cu_err]).transpose()
    print

 #   P_W2 = P_S2 / cos_2
 #   P_W2_err = np.sqrt(P_S2_err**2 + P_Cu_err**2)
 #   print "P_W2"
 #   print np.array([P_W2, P_W2_err]).transpose()
 #   print
    P_W2_err = np.ones(P_W2.size) * P_err

    eta = P_W2 / P_W1
    eta_err = np.sqrt(
        (1.0 / P_W1 * P_W2_err)**2
        + (P_W2 / (P_W1**2) * P_W1_err)**2
    )
    print "η"
    print np.array([eta, eta_err]).transpose()
    print

    P_v = P_W1 - P_W2
    P_v_err = np.sqrt(P_W1_err**2 + P_W2_err**2)
    print "P_v"
    print np.array([P_v, P_v_err]).transpose()
    print

    P_Fe = P_v - P_Cu
    P_Fe_err = np.sqrt(P_v_err**2 + P_Cu_err**2)
    print "P_Fe"
    print np.array([P_Fe, P_Fe_err]).transpose()
    print

    P_S1 = U_1 * I_1
    P_S1_err = np.sqrt(
        (U_1 * I_err)**2
        + (I_1 * U_err)**2
    )
    print "P_S1"
    print np.array([P_S1, P_S1_err]).transpose()
    print

    U_2_err = np.ones(U_2.size) * U_err
    U_1_err = np.ones(U_2.size) * U_err

    transfer = U_2 / U_1
    transfer_err = np.sqrt(
        (1.0 / U_1 * U_2_err)**2
        + (U_2 / (U_1**2) * U_1_err)**2
    )

    dtype = map(lambda x: (x, "f8"), [
        "I_2", "I_2_err",
        "P_S2", "P_S2_err",
        "P_Cu", "P_Cu_err",
        "eta", "eta_err",
        "P_v", "P_v_err",
        "P_Fe", "P_Fe_err",
        "P_S1", "P_S1_err",
    ])

    export = np.zeros(I_2.shape, dtype=dtype)

    export["I_2"] = I_2
    export["I_2_err"] = I_2_err
    export["P_S2"] = P_S2
    export["P_S2_err"] = P_S2_err
    export["P_Cu"] = P_Cu
    export["P_Cu_err"] = P_Cu_err
    export["eta"] = eta
    export["eta_err"] = eta_err
    export["P_v"] = P_v
    export["P_v_err"] = P_v_err
    export["P_Fe"] = P_Fe
    export["P_Fe_err"] = P_Fe_err
    export["P_S1"] = P_S1
    export["P_S1_err"] = P_S1_err

    np.savetxt("export.csv", export, fmt="%f")

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, P_Cu, xerr=I_2_err, label=ur"$P_\mathrm{Cu}$", yerr=P_Cu_err, **plotargs)
    pl.errorbar(I_2, P_S2, xerr=I_2_err, label=ur"$P_{S,2}$", yerr=P_S2_err, **plotargs)
    pl.errorbar(I_2, P_v,  xerr=I_2_err, label=ur"$P_v$", yerr=P_v_err, **plotargs)
    pl.errorbar(I_2, P_W2, xerr=I_2_err, label=ur"$P_{W,2}$", yerr=P_W2_err, **plotargs)
    pl.errorbar(I_2, P_W1, xerr=I_2_err, label=ur"$P_{W,1}$", yerr=P_W1_err, **plotargs)
    pl.errorbar(I_2, P_Fe, xerr=I_2_err, label=ur"$P_\mathrm{Fe}$", yerr=P_Fe_err, **plotargs)
    pl.title(u"Leistungen gegen Sekundärstrom")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.ylabel(ur"$P / \mathrm{W}$")
    pl.legend(loc="upper left")
    pl.savefig("d.pdf")

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, eta, label=ur"$\eta$", xerr=I_2_err, yerr=eta_err, **plotargs)
    pl.title(u"Wirkungsgrad gegen Sekundärstrom")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.ylabel(ur"$\eta$")
    pl.savefig("eta.pdf")

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, transfer, xerr=I_2_err, yerr=transfer_err, **plotargs)
    pl.title(u"Spannungsübertragung")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.ylabel(ur"$U_2 / U_1$")
    pl.savefig("g.pdf")

    m = np.argmin(np.abs(U_1 / I_1 - U_2/I_2 / np.sqrt(2)))
    print "Minimaler Wert bei", m
    print "ωL =", U_2[m] / I_2[m]

    m = np.argmin(np.abs(I_2 / I_1 - 1 / np.sqrt(2)))
    print "Minimaler Wert bei", m
    print "ωL =", U_2[m] / I_2[m] + R_1 + R_2

    print

    omegaL_list = np.array([176.309, 97, 87])
    sigma_list = [
        (0.328, 0.0329),
        (0.036, 0.0293),
        (0.0408, 0.0154),
        (0.0771, 0.0271),
    ]

    omegaL = 114.0
    omegaL_err = 40.0

    sigma = sum([z / s**2 for z, s in sigma_list]) / sum([1 / s**2 for z, s in sigma_list])
    sigma_err = len(sigma_list) / sum([1 / s**2 for z, s in sigma_list])

    print sigma, sigma_err

    R = U_2 / I_2

    ML = np.sqrt(1 - sigma)
    U2U1 = R / (R + 2 * R_1) * ML / np.sqrt(1 + (sigma * omegaL / (R + 2 * R_1))**2)
    U2U1_err = np.sqrt(

        (-((omegaL * R * np.sqrt(1 - sigma) *  sigma**2)/((R + 2 * R_1)**3 * (1 + (omegaL**2 * sigma**2)/(R + 2 * R_1)**2)**(3.0/2))) * omegaL_err)**2

        +(-((omegaL**2 * R * np.sqrt(1 - sigma) * sigma)/((R + 2 * R_1)**3 * (1 + (omegaL**2 * sigma**2)/(R + 2 * R_1)**2)**( 3.0/2))) - R/( 2 * (R + 2 * R_1) * np.sqrt(1 - sigma) * np.sqrt( 1 + (omegaL**2 * sigma**2)/(R + 2 * R_1)**2)) * sigma_err)**2

    )

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, transfer, xerr=I_2_err, label="gemessen", yerr=transfer_err, **plotargs)
    pl.errorbar(I_2, U2U1, xerr=I_2_err, yerr=U2U1_err, label="errechnet", **plotargs)
    pl.title(u"Spannungsübertragung")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.ylabel(ur"$U_2 / U_1$")
    pl.legend()
    pl.savefig("g.pdf")

if __name__ == "__main__":
    a()
    c()
