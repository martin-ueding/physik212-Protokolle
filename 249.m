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
0.02	111	2.03	2.23
0.03	119	1.40	1.40
0.04	146	1.22	1.24
0.05	146	1.46	1.03
0.02	113	2.15	2.34
0.03	173	1.82	1.84
0.04	173	1.33	1.32
0.045	197	1.27	1.31
0.05	208	1.17	1.21
0.04	208	1.47	1.51
];

faden.U.err = 2.0;
faden.r.err = 0.003;
faden.I.err = 0.02;

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
.5e-3	7.47	.5e-3	2.47	.5e-3	6.72
];

millikan(2).data = [
.5e-3	6.47	.5e-3	2.34	.5e-3	3.22
];

millikan(3).data = [
.5e-3	10.34	.5e-3	3.44	.5e-3	5.38
];

millikan(4).data = [
.5e-3	7.01	.5e-3	1.78	.5e-3	1.72
];

millikan(5).data = [
.5e-3	10.85	.5e-3	3.94	.5e-3	5
];

millikan(6).data = [
.5e-3	13.08	.5e-3	1.47	.5e-3	1.52
];

millikan(7).data = [
.5e-3	3.34	.5e-3	10.91	.5e-3	1.32
];

millikan(8).data = [
.5e-3	5.35	.5e-3	1.72	.5e-3	1.03
];

#millikan(9).data = [
#.1e-3	0.9	.1e-3	1.1	.1e-3	1.1
#];
#
#millikan(10).data = [
#.1e-3	2.9	.1e-3	1.5	.1e-3	1.5
#];
#
#millikan(11).data = [
#.1e-3	2.6	.1e-3	0.9	.1e-3	0.9
#];

s.err = 1.0e-4;
t.err = 0.1;

# Das elektrische Feld in [V/m].
E.val = 500 / 7.75e-2;
E.err = 0.1;

###############################################################################
#                               Literaturwerte                                #
###############################################################################

luft.data = [
0	17.20e-6
20	18.19e-6
40	19.12e-6
];

rho.oel.val = 700;
rho.luft.val = 1;

g = 9.81;

###############################################################################
#                                 Funktionen                                  #
###############################################################################

function e = rel_error(v)
	e = v.err / v.val;
end

###############################################################################
#                                 Einleitung                                  #
###############################################################################

printf("###########\n");
printf("Versuch 249\n");
printf("###########\n");
printf("\n");

###############################################################################
#                         Rechnungen Fadenstrahlrohr                          #
###############################################################################

plot_x = faden.data(:, 1) .^2 .* (0.5 .* (faden.data(:, 2) + faden.data(:, 3))) .^2;
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

printf("α₁ = %.2e ± %.2e (%.1e)\n", alpha1.val, alpha1.err, rel_error(alpha1));
printf("B_E = %.2e ± %.2e (%.1e) T\n", B_E.val, B_E.err, rel_error(B_E));

clf;
hold on;

p1 = errorbar(plot_x, plot_y, plot_error, "~.k");
p2 = plot(function_x, function_y, "-k");

set(gca(), "fontsize", 20);
xlabel("r^2 I^2  / [m^2  A^2 ]");
ylabel("U / [V]");
set(p1, "linestyle", "none");
set(p1, "marker", "+");
title("Fadenstrahlrohr");

print("fadenstrahl.eps", "-tight");

em.val = 2/.716^2 * R.val^2 / n.val^2 / mu0.val^2 * alpha1.val;
em.err = sqrt(sum([
			(2/.716^2 * R.val / n.val^2 / mu0.val^2 * alpha1.val * R.err )^2
			(2/.716^2 * R.val / n.val^2 / mu0.val^2 * alpha1.err)^2
			]));

printf("e/m = %.2e ± %.2e (%.1e) C/kg\n", em.val, em.err, rel_error(em));

###############################################################################
#                         Rechnungen Millikanversuch                          #
###############################################################################

printf("\n");
printf("Millikanversuch\n");
printf("===============\n");
printf("\n");
printf("Luftviskosität\n");
printf("--------------\n");
printf("\n");

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
xlabel("T / [^{\circ} C]");
ylabel("\eta / [Pa s]");
set(p1, "linestyle", "none");
set(p1, "marker", "+");
# FIXME Umlaut im Titel, Encoding richtig einstellen.
title("Viskosität von Luft");

print("luft.eps", "-tight");

printf("alpha_0 = %.3g, alpha_1 = %.3g\n", par(1), par(2));

luft.eta.val = luft_fit_function(luft.T.val, par);

printf("eta_Luft = %.3g Pa\n", luft.eta.val);

# Nun die Sedimentgeschwindigkeiten.

printf("\n");
printf("Tabelle mit den verrechneten drei Geschwindigkeiten pro Teilchen\n");
printf("----------------------------------------------------------------\n");
printf("\n");

printf(" k       v_\\circ            v_\\Downarrow          v_\\Uparrow       n\n");

v3_array.val = [];
v3_array.err = [];

# Gehe durch alle Tröpfchen $k$ durch.
for k = 1:length(millikan)
	data = millikan(k).data;

	v.val = [data(:, 1) ./ data(:, 2) data(:, 3) ./ data(:, 4) data(:, 5) ./ data(:, 6)];

	e1 = sqrt(
		(1 ./ data(:, 2) .* s.err).^2
		+ (data(:, 1) ./ (data(:, 2).^2) .* t.err).^2
	);
	e2 = sqrt(
		(1 ./ data(:, 4) .* s.err).^2
		+ (data(:, 3) ./ (data(:, 4).^2) .* t.err).^2
	);
	e3 = sqrt(
		(1 ./ data(:, 6) .* s.err).^2
		+ (data(:, 5) ./ (data(:, 6).^2) .* t.err).^2
	);
	v.err = [e1 e2 e3];

	v2.val = [];
	v2.err = [];

	n = 0;

	#for j = 1:length(v.val)
		row.val = v.val;
		row.err = v.err;

		# Prüfe, ob $2 v_\circ = v_\Downarrow - v_\Uparrow$ gilt.
		deviation = 2 * row.val(1) - row.val(2) + row.val(3);
		deviation_erlaubt = 2 * row.err(1) + row.err(2) + row.err(3);

		if abs(deviation) <= abs(deviation_erlaubt)
			#printf("Messung %d von Teilchen %d: %.2e ≤ %.2e\n", j, k, deviation, deviation_erlaubt);
			n += 1;
			v2.val = [v2.val ; row.val];
			v2.err = [v2.err ; row.err];
		else
			#printf("Verwerfe Messung\n");
		endif
	#endfor

	if n == 0
		printf("Keine brauchbaren Messungen für Teilchen %d.\n", k);
		continue;
	elseif n == 1
		v3 = v2;
	else
		v3.val = mean(v2.val);
		v3.err = sqrt(sumsq(v2.val)) / n;
	endif

	printf("%2d: %.2e ± %.2e, %.2e ± %.2e, %.2e ± %.2e, %d \n",
			k,
			v3.val(1),
			v3.err(1),
			v3.val(2),
			v3.err(2),
			v3.val(3),
			v3.err(3),
			n
		  );

	v3_array.val = [v3_array.val ; v3.val];
	v3_array.err = [v3_array.err ; v3.err];
endfor

rq.val = [];
rq.err = [];

printf("\n");
printf("Tabelle mit Radius und Ladung\n");
printf("-----------------------------\n");
printf("\n");

for k = 1:length(v3_array.val)
	v3.val = v3_array.val(k, :);
	v3.err = v3_array.err(k, :);

	r.val = sqrt( (v3.val(2) - v3.val(3) ) * (9 * luft.eta.val) / (4 * g * (rho.oel.val - rho.luft.val)));
	r.err = (1 / (2 * r.val)) * (9 * luft.eta.val) / (4 * g * (rho.oel.val - rho.luft.val)) * sqrt( v3.err(2)^2 + v3.err(3)^2 );

	q.val = 3 * pi * luft.eta.val * r.val * (v3.val(2) + v3.val(3)) / E.val;
	q.err = sqrt(
			(3 * pi * luft.eta.val * r.val / E.val)^2 * (v3.err(2)^2 + v3.err(3)^2)
			+ (q.val / E.val^2 * E.err)^2
			);

	printf("r = %.2e ± %.2e (%+.1e), q = %.2e ± %.2e (%+.1e)\n", r.val, r.err, rel_error(r), q.val, q.err, rel_error(q));

	rq.val = [rq.val ; r.val q.val];
	rq.err = [rq.err ; r.err q.err];
end

printf("\n");

printf("Suche nach Elementarladung\n");
printf("--------------------------\n");
printf("\n");

# Sortiere die Einträge nach Ladung $q$.
[sorted, indexes] = sort(rq.val);

for i = 1:length(indexes)
	k = indexes(i, 2);
	printf("r = %.2e m, q = %.2e C\n", rq.val(k, 1), rq.val(k, 2));

	div(i).r.val = rq.val(k, 1);
	div(i).q.val = rq.val(k, 2);
	div(i).r.err = rq.err(k, 1);
	div(i).q.err = rq.err(k, 2);
end

printf("\n");

# Nun ist div ein Array mit jeweils einem Struct mit $e$ und $q$, die jeweils
# wieder ``val`` und ``err`` enthalten.

printf("Suche nach gemeinsamen Nenner\n");
printf("-----------------------------\n");
printf("\n");

# Jetzt bilde ich die Quotienten $q_k/q_0$.
for k = 1:length(div)
	div(k).ratio.val = div(k).q.val / div(1).q.val;
	div(k).ratio.err = sqrt(
			(1 / div(1).q.val * div(k).q.err)^2
			+ (div(k).q.val / div(1).q.val^2 * div(1).q.err)^2
			);

	# Finde einen Bruch, der bis auf den Messfehler das Verhältnis annähert.
	[div(k).a div(k).b] = rat(div(k).ratio.val, div(k).ratio.err);

	printf("%.2g ± %.1g → %d / %d\n", div(k).ratio.val, div(k).ratio.err, div(k).a, div(k).b);

	lcm_input(k) = div(k).b;
end

printf("\n");

v = lcm(lcm_input);

printf("v = %d\n", v);
printf("\n");

for k = 1:length(div)
	div(k).n.val = div(k).a * v / div(k).b;
	div(k).es.val = div(k).q.val / div(k).n.val;

	printf("k = %d, e_S = %.3g C, n = %d, r = %.3g ± %.3g\n",
			k,
			div(k).es.val,
			div(k).n.val,
			div(k).r.val,
			div(k).r.err
		  );
end

printf("\n");

# -----------------------------------------------------------------------------

# Konvertiere Daten für den nächsten Abschnitt.

printf("Cunninghamkorrektur\n");
printf("-------------------\n");
printf("\n");

for k = 1:length(div)
	er.val(k, :) = [div(k).es.val div(k).r.val];
	er.err(k, :) = [0             div(k).r.err];
end

function y = cunningham(x, par)
	y = par(1) + par(2) * x;
end

plot_x = (1 ./ er.val(:, 2));
plot_y = (er.val(:, 1).^(2/3));
plot_error = abs(2/3 .* (er.val(:, 1)).^(2/3-1) .* er.err(:, 1));

[f, par, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		plot_x,
		plot_y,
		[1, 1],
		"cunningham",
		0.001,
		20
		);

alpha0.val = par(1);
alpha0.err = sqrt(diag(covp))(1);

alpha1.val = par(2);
alpha1.err = sqrt(diag(covp))(2);

printf("α₀ = %.2e ± %.2e (%.1e)\n", alpha0.val, alpha0.err, rel_error(alpha0));
printf("α₁ = %.2e ± %.2e (%.1e)\n", alpha1.val, alpha1.err, rel_error(alpha1));

e.val = abs(alpha0.val)^(3.0/2.0);
e.err = abs(3/2 * abs(alpha0.val)^(3/2-1) * alpha0.err);

printf("e = %.2e ± %.2e (%.1e) C\n", e.val, e.err, rel_error(e));

function_x = (0 : (max(plot_x)-min(plot_x))/10 : max(plot_x))';
function_y = cunningham(function_x, par);

clf;
hold on;

p1 = errorbar(plot_x, plot_y, plot_error, "~.k");
p2 = plot(function_x, function_y, "-k");

set(gca(), "fontsize", 20);
set(p1, "linestyle", "none");
xlabel("1/r / [1/m]");
ylabel("e_S^{2/3} / [C^{2/3}]");
set(p1, "marker", "x");
title("Cunningham");

print("cunningham.eps", "-tight");

###############################################################################
#                              Rechnungen Finale                              #
###############################################################################

m.val = e.val / em.val;
m.err = sqrt(
	(1/em.val * e.err)^2
+ (e.val / em.val^2 * em.err)^2
);

printf("\n");
printf("gemeinsam\n");
printf("=========\n");
printf("\n");

printf("m = %.2e ± %.2e (%.1e) kg", m.val, m.err, rel_error(m));
