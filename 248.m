#!/usr/bin/octave -fq
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

###############################################################################
#                                  Messdaten                                  #
###############################################################################

raw = load("Ueding-Hysterese.txt");

data = [
-raw(:, 2) raw(:, 3)/1000
];

Delta_I = .01;

l.val = .477;
l.err = .004;

d.val = 2e-3;
d.err = .05e-3;

N.val = 1000;

###############################################################################
#                               Literaturwerte                                #
###############################################################################

mu0.val = pi / 2500000;

###############################################################################
#                                 Rechnungen                                  #
###############################################################################

I.val = data(:, 1);
B.val = data(:, 2);
I.err = ones(size(I.val)) * Delta_I;
B.err = B.val * 0.03;

H.val = N.val .* I.val ./ l.val .- d.val .* B.val ./ (mu0.val .* l.val);
H.err = sqrt(
		(N.val ./ l.val .* I.err).^2
		+ ((- N.val .* I.val ./ (l.val .^2) .+ d.val .* B.val ./ (mu0.val .* (l.val.^2))) * l.err).^2
		+ (B.val ./ (mu0.val .* l.val) .* d.err).^2
		+ (d.val ./ (mu0.val .* l.val) .* B.err).^2
		);

hold on;

#p1 = errorbar(H.val, B.val, H.err, B.err, "~>.k");
p1 = plot(H.val, B.val);
set(gca(), "fontsize", 15);
xlabel("H in [A/m]");
ylabel("B in [T]");
set(p1, "linestyle", "none");
set(p1, "marker", ".");
grid()
title("Hysterese");

print("hysterese.eps", "-tight");

mm = 0;
j = 0;

for i = 100:1000
	m = B.val(i) / H.val(i);

	if (m > mm)
		mm = m;
		j = i;
	endif
endfor


mumax.val = mm / mu0.val;
mumax.err = sqrt(
		(B.err(j) / (H.val(j)^2) * H.err(j))^2
		+ (1 / H.val(j) * B.err(j))^2
		) / mu0.val;

printf("μ_max = %.4g ± %.2g μ₀\n", mumax.val, mumax.err);

printf("Benutzter Messwert: H = %.4g ± %.2g, B = %.4g ± %.2g\n", H.val(j), H.err(j), B.val(j), B.err(j));

clf;

hold on
p1 = errorbar(H.val(1:1000), B.val(1:1000), B.err(1:1000));
set(gca(), "fontsize", 15);
xlabel("H in [A/m]");
ylabel("B in [T]");
set(p1, "linestyle", "none");
set(p1, "marker", "+");
set(p1, "markersize", 5);
grid()
plot([0; 1500], [0; 1500*mm], "-k");
title("Hysterese, erste 1000 Messwerte");
print("hysterese-1000.eps", "-tight");


mm = -inf;
j = -inf;

for i = 116:116
	m = B.val(i) / H.val(i);

	if (m > mm)
		mm = m;
		j = i;
	endif
endfor

mua.val = mm / mu0.val;
mua.err = sqrt(
		(B.err(j) / (H.val(j)^2) * H.err(j))^2
		+ (1 / H.val(j) * B.err(j))^2
		) / mu0.val;

printf("μ_A = %.4g ± %.2g μ₀\n", mua.val, mua.err);

printf("Benutzter Messwert: H = %.4g ± %.2g, B = %.4g ± %.2g\n", H.val(j), H.err(j), B.val(j), B.err(j));

clf;

limit = 200;

hold on
p1 = errorbar(H.val(1:limit), B.val(1:limit), B.err(1:limit));
set(gca(), "fontsize", 15);
xlabel("H in [A/m]");
ylabel("B in [T]");
set(p1, "linestyle", "none");
set(p1, "marker", "+");
set(p1, "markersize", 5);
grid()
p2 = plot([0; max(H.val(1:limit))], [0; max(H.val(1:limit))*mm], "k");
set(p2, "linestyle", "--");
title("Hysterese, erste 400 Messwerte");
print("hysterese-mua.eps", "-tight");
