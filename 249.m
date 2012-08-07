#!/usr/bin/octave -q
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

###############################################################################
#                                  Messwerte                                  #
###############################################################################

# Lufttemperatur [°C].
luft.T.val = 20;
luft.T.err = 0.1;

millikan.

###############################################################################
#                               Literaturwerte                                #
###############################################################################

luft.data = [
0	17.20e-6
20	18.19e-6
40	19.12e-6
];

###############################################################################
#                                 Rechnungen                                  #
###############################################################################

# Errechne die Viskosität von Luft anhand eines linearen Fits.

function eta = luft_fit_function(T, par)
	eta = par(1) + par(2) * T;
end

# Erzeuge einen Plot von den Werten.
title("Viskosität von Luft");
luft.plot = plot(luft.data(:, 1), luft.data(:, 2), "+k", luft.data(:, 1), luft.data(:, 2), "-k");
#set(luft.plot, "linestyle", "none");
print("luft.eps", "-tight");

[f, p, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		luft.data(:, 1),
		luft.data(:, 2),
		[1, 1],
		"luft_fit_function",
		0.001,
		20
		);

luft.eta.val = luft_fit_function(luft.T.val, p);
