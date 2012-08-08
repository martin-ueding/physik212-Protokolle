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
#                          Messwerte Fadenstrahlrohr                          #
###############################################################################

# Daten von Fadenstrahlrohr. Erste Spalte ist $r$ in [m], zweite $U$ in [V],
# dritte $I_1$ in A und die letzte $I_1$ in A.
faden.data = [
0.02   0.14734   0.21169   0.94109
0.02   0.1523772   0.3873263   0.1532324
0.03   0.37048   0.63075   0.94510
0.03   0.8603026   0.4372725   0.0509417
0.04   0.0025177   0.7107548   0.7497745
0.04   0.54712   0.28614   0.86428
0.05   0.43760   0.43785   0.70058
0.05   0.8823911   0.1423691   0.4405897
];

faden.U.err = 0.01;
faden.r.err = 0;
faden.I.err = 0;

R.val = 2.1;
R.err = 0;

n.val = 20;

mu0.val = 4 * pi * 10^-7;

###############################################################################
#                          Messwerte Millikanversuch                          #
###############################################################################

# Lufttemperatur [°C].
luft.T.val = 20;
luft.T.err = 0.1;

# Messwerte aus dem Millikanversuch. Dabei sind immer zwei Spalten ein Tupel
# aus $s$ und $t$ in [m] und [s]. Das erste Tupel ist $s_\circ$, das zweite
# $s_\Downarrow$ und das dritte $s_\Uparrow$.
millikan(1).data = [
0.769065   0.322802   0.339114   0.239415   0.032507   0.264501
0.171696   0.328840   0.345539   0.087307   0.384054   0.464782
0.272618   0.977087   0.725682   0.078994   0.559948   0.296917
0.144843   0.691315   0.209988   0.018873   0.654417   0.438635
0.913738   0.750571   0.026533   0.705835   0.067015   0.446933
];

millikan(2).data = [
0.537090   0.755126   0.733435   0.376961   0.451800   0.619722
0.316983   0.377428   0.659851   0.886051   0.579992   0.137841
0.118771   0.999849   0.498004   0.736818   0.781862   0.204266
0.309962   0.752552   0.154147   0.464276   0.067827   0.138121
0.477897   0.073085   0.835708   0.085530   0.342070   0.413357
];

millikan(3).data = [
0.100252   0.122972   0.841049   0.461951   0.252597   0.966471
0.827113   0.459299   0.712585   0.956165   0.921312   0.432508
0.447464   0.812215   0.138149   0.839850   0.069354   0.994035
0.689454   0.619314   0.046696   0.990169   0.648663   0.607209
0.828994   0.713073   0.942968   0.821535   0.197838   0.876198
];

millikan(4).data = [
0.040231   0.856706   0.636383   0.827458   0.501007   0.903331
0.320850   0.957510   0.937860   0.569142   0.172456   0.104701
0.597103   0.841585   0.701413   0.050277   0.378254   0.512957
0.891816   0.266735   0.808601   0.080381   0.083243   0.160874
0.524568   0.149159   0.270007   0.426659   0.414475   0.773191
];

millikan(5).data = [
0.504355   0.861836   0.782336   0.345395   0.349991   0.086313
0.922832   0.078809   0.380788   0.841462   0.284642   0.592690
0.962133   0.112430   0.410826   0.391488   0.519649   0.225896
0.627501   0.053451   0.629298   0.373784   0.466685   0.402641
0.115311   0.874136   0.476231   0.756763   0.548896   0.333194
];

millikan(6).data = [
0.912888   0.104703   0.172450   0.866119   0.712690   0.371106
0.221956   0.935233   0.852571   0.576827   0.936937   0.702772
0.030127   0.211322   0.937679   0.524534   0.704310   0.177216
0.578679   0.943694   0.220905   0.604986   0.885215   0.582653
0.280431   0.681162   0.084029   0.112917   0.996824   0.655161
];

millikan(7).data = [
0.183817   0.654073   0.770994   0.753128   0.119528   0.706488
0.275338   0.172152   0.944487   0.450018   0.853694   0.220270
0.756365   0.726178   0.273989   0.311923   0.090295   0.095377
0.814681   0.693134   0.873913   0.433167   0.929500   0.923229
0.678683   0.960346   0.150116   0.595203   0.327940   0.493895
];

millikan(8).data = [
0.828841   0.461007   0.475153   0.575983   0.048116   0.598715
0.263666   0.446413   0.578424   0.917226   0.251722   0.430963
0.665534   0.637549   0.815294   0.744109   0.491356   0.017354
0.740351   0.637792   0.935218   0.548379   0.522549   0.243779
0.246143   0.754952   0.237065   0.870975   0.219933   0.971574
];

millikan(9).data = [
0.265270   0.070369   0.252364   0.736098   0.379166   0.760903
0.059551   0.981854   0.125479   0.578624   0.925271   0.360239
0.408921   0.554691   0.033956   0.307532   0.882394   0.794362
0.705472   0.244892   0.216324   0.290161   0.507098   0.482792
0.984887   0.928714   0.105984   0.529714   0.821012   0.982573
];

millikan(10).data = [
0.319412   0.445241   0.963858   0.414228   0.541015   0.942100
0.346803   0.029649   0.616791   0.510756   0.397634   0.364609
0.237391   0.115260   0.047568   0.628866   0.397384   0.723407
0.556194   0.869858   0.931872   0.440158   0.990766   0.886283
0.358030   0.941087   0.546437   0.627175   0.910649   0.925230
];

s.err = 0.1;
t.err = 0.1;

###############################################################################
#                               Literaturwerte                                #
###############################################################################

luft.data = [
0	17.20e-6
20	18.19e-6
40	19.12e-6
];

###############################################################################
#                                 Funktionen                                  #
###############################################################################

function e = rel_error(v)
	e = v.err / v.val;
end

printf("###########\n");
printf("Versuch 249\n");
printf("###########\n");
printf("\n");

###############################################################################
#                         Rechnungen Fadenstrahlrohr                          #
###############################################################################

plot_x = faden.data(:, 1) .^2 .* 0.5 .* (faden.data(:, 2) + faden.data(:, 3)) .^2;
plot_y = faden.data(:, 2);
plot_error = ones(size(faden.data(:, 1))) * faden.U.err;

function U = faden_funktion(rIsq, par)
	U = par(1) * rIsq;
end

[f, par, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		plot_x,
		plot_y,
		[1],
		"faden_funktion",
		0.001,
		20
		);

function_x = (min(plot_x) : (max(plot_x)-min(plot_x))/10 : max(plot_x))';
function_y = faden_funktion(function_x, par);

alpha1.val = par(1);
alpha1.err = sqrt(diag(covp))(1);

B_E.list = 0.5 .* (faden.data(:, 2) + faden.data(:, 3));
B_E.val = mean(B_E.list);
B_E.err = std(B_E.list) / length(B_E.list);

printf("Fadenstrahlrohr\n");
printf("===============\n");
printf("\n");

printf("α₁ = %.3g ± %.3g (%.2g)\n", alpha1.val, alpha1.err, rel_error(alpha1));
printf("B_E = %.3g ± %.3g (%.2g) T\n", B_E.val, B_E.err, rel_error(B_E));

hold on;

p1 = errorbar(plot_x, plot_y, plot_error, "~.k");
p2 = plot(function_x, function_y, "-k");

set(gca(), "fontsize", 20);
set(p1, "linestyle", "none");
set(p1, "marker", "+");
title("Fadenstrahlrohr");

print("fadenstrahl.eps", "-tight");

em.val = 2/.716^2 * R.val^2 / n.val^2 / mu0.val^2 * alpha1.val;
em.err = sqrt(sum([
			(2/.716^2 * R.val / n.val^2 / mu0.val^2 * alpha1.val * R.err )^2
			(2/.716^2 * R.val / n.val^2 / mu0.val^2 * alpha1.err)^2
			]));

printf("e/m = %.3g ± %.3g (%.2g) C/kg\n", em.val, em.err, rel_error(em));

###############################################################################
#                         Rechnungen Millikanversuch                          #
###############################################################################

# Errechne die Viskosität von Luft anhand eines linearen Fits.

function eta = luft_fit_function(T, par)
	eta = par(1) + par(2) * T;
end

[f, par, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		luft.data(:, 1),
		luft.data(:, 2),
		[1, 1],
		"luft_fit_function",
		0.001,
		20
		);

plot_x = luft.data(:, 1);
plot_y = luft.data(:, 2);
plot_error = ones(size(plot_y)) * 0;

function_x = (min(plot_x) : (max(plot_x)-min(plot_x))/10 : max(plot_x))';
function_y = luft_fit_function(function_x, par);

# Erzeuge einen Plot von den Werten.
clf;
hold on;

p1 = errorbar(plot_x, plot_y, plot_error, "~.k");
p2 = plot(function_x, function_y, "-k");

set(gca(), "fontsize", 20);
set(p1, "linestyle", "none");
set(p1, "marker", "+");
# FIXME Umlaut im Titel, Encoding richtig einstellen.
title("Viskosität von Luft");

print("luft.eps", "-tight");

luft.eta.val = luft_fit_function(luft.T.val, par);

# Nun die Sedimentgeschwindigkeiten.

printf("\n");
printf("Millikanversuch\n");
printf("===============\n");
printf("\n");
printf("Tabelle mit den verrechneten drei Geschwindigkeiten pro Teilchen\n");
printf("----------------------------------------------------------------\n");
printf("\n");

printf(" k          v_\\circ             v_\\Downarrow           v_\\Uparrow        n\n");

# Gehe durch alle Tröpfchen $k$ durch.
for k = 1:length(millikan)
	data = millikan(k).data;

	v.val = [data(:, 1) ./ data(:, 2) data(:, 3) ./ data(:, 4) data(:, 5) ./ data(:, 6)];

	e1 = sqrt(
		(1 ./ data(:, 2) .* s.err).^2
		+ (data(:, 2) ./ (data(:, 2).^2) .* t.err).^2
	);
	e2 = sqrt(
		(1 ./ data(:, 4) .* s.err).^2
		+ (data(:, 4) ./ (data(:, 4).^2) .* t.err).^2
	);
	e3 = sqrt(
		(1 ./ data(:, 6) .* s.err).^2
		+ (data(:, 6) ./ (data(:, 6).^2) .* t.err).^2
	);
	v.err = [e1 e2 e3];

	v2.val = [];
	v2.err = [];

	n = 0;

	for j = 1:length(v.val)
		row.val = v.val(j, :);
		row.err = v.err(j, :);

		# Prüfe, ob $2 v_\circ = v_\Downarrow - v_\Uparrow$ gilt.
		deviation = 2 * row.val(1) - row.val(2) + row.val(3);
		deviation_erlaubt = 2 * row.err(1) + row.err(2) + row.err(3);


		if abs(deviation) <= abs(deviation_erlaubt)
			#printf("Messung %d von Teilchen %d: %.3g ≤ %.3g\n", j, k, deviation, deviation_erlaubt);
			n += 1;
			v2.val = [v2.val ; row.val];
			v2.err = [v2.err ; row.err];
		else
			#printf("Verwerfe Messung\n");
		endif
	endfor

	if n == 0
		#printf("Keine brauchbaren Messungen für Teilchen %d.\n", k);
		continue;
	elseif n == 1
		v3 = v2;
	else
		v3.val = mean(v2.val);
		v3.err = sqrt(sumsq(v2.val)) / n;
	endif

	printf("%2d: %.3e ± %.3e, %.3e ± %.3e, %.3e ± %.3e, %d \n",
			k,
			v3.val(1),
			v3.err(1),
			v3.val(2),
			v3.err(2),
			v3.val(3),
			v3.err(3),
			n
		  );
endfor
