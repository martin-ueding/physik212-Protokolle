#!/usr/bin/octave -q
# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

###############################################################################
#                                  Messwerte                                  #
###############################################################################

# Lufttemperatur [°C].
luft.T.val = 20;
luft.T.err = 0.1;

###############################################################################
#                               Literaturwerte                                #
###############################################################################

luft.data = [
0	17.20
20	18.19
40	19.12
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
print("luft.eps");

[f, p, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		luft.data(:, 1),
		luft.data(:, 2),
		[1, 1],
		"luft_fit_function",
		0.001,
		20
		);

luft.eta.val = luft_fit_function(luft.T.val, p);
