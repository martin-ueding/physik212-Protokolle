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

I_err = 0.5
P_err = 0.5
R_err = 0.5
U_err = 0.5

plotargs = {
    "color": "black",
    "linestyle": "None",
    "markeredgecolor": "black",
    "markersize": 7
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
        30.79,
        37.63,
        35.87,
        34.06,
        31.71,
        29.35,
    ])
    U = d["U_2"]
    R = U_R / I

    ###########################################################################
    #                               Rechnungen                                #
    ###########################################################################

    P_S = I * U
    cos = U_R / U

    pl.clf()
    pl.grid(True)
    pl.errorbar(I, P_S, label=ur"$P_S$", yerr=np.ones(P_S.size) * P_err, marker="x", **plotargs)
    pl.errorbar(I, P_W, label=ur"$P_W$", yerr=np.ones(P_W.size) * P_err, marker="o", **plotargs)
    pl.errorbar(I, P_S * cos, label=ur"$P_S \cos(\phi)$", yerr=np.ones(P_W.size) * P_err, marker="d", **plotargs)
    pl.title(u"Leistungen gegen Strom")
    pl.xlabel(ur"$I / \mathrm{A}$")
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


    R_1 = R_2 = 0.5

    ###########################################################################
    #                               Rechnungen                                #
    ###########################################################################

    P_W1_err = np.ones(P_W1.shape) * P_err

    P_S2 = U_2 / I_2
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

    P_W2 = P_S2 - P_Cu
    P_W2_err = np.sqrt(P_S2_err**2 + P_Cu_err**2)
    print "P_W2"
    print np.array([P_W2, P_W2_err]).transpose()
    print

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

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, P_W1, label=ur"$P_{W,1}$", yerr=P_W1_err, **plotargs)
    pl.errorbar(I_2, P_W2, label=ur"$P_{W,2}$", yerr=P_W2_err, **plotargs)
    pl.errorbar(I_2, P_v, label=ur"$P_v$", yerr=P_v_err, **plotargs)
    pl.errorbar(I_2, P_Cu, label=ur"$P_\mathrm{Cu}$", yerr=P_Cu_err, **plotargs)
    pl.errorbar(I_2, P_Fe, label=ur"$P_\mathrm{Fe}$", yerr=P_Fe_err, **plotargs)
    pl.title(u"Diverses gegen Sekundärstrom")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.legend()
    pl.savefig("d.pdf")

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, eta, label=ur"$\eta$", yerr=eta_err, **plotargs)
    pl.title(u"Wirkungsgrad gegen Sekundärstrom")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.ylabel(ur"$\eta$")
    pl.savefig("eta.pdf")

    pl.clf()
    pl.grid(True)
    pl.errorbar(I_2, transfer, yerr=transfer_err, **plotargs)
    pl.title(u"Spannungsübertragung")
    pl.xlabel(ur"$I_2 / \mathrm{A}$")
    pl.ylabel(ur"$U_2 / U_1$")
    pl.savefig("g.pdf")

if __name__ == "__main__":
    a()
    c()
