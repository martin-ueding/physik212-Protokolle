#!/usr/bin/octave -q
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

phi.err = 5;

# Widerstand R in [Ohm] und φ in [rad].
c.data.val = [
200		179
300		141
400		117
500		100
600		86
700		76
800		68
900		62
1000	57
];

c.R1.val = 1000;
c.R1.err = 10;

c.R2.val = 50;
c.R2.err = 1;

c.U0.val = 2.01;
c.U0.err = 0.1;

# Zeit in [s] und φ in [rad].
h.data.val = [
1.00	65
1.75	60
1.75	61
2.28	56
3.13	52
3.94	48
5.16	44
5.85	40
13.35	20
];

h.C.val = 10.21e-6;
h.C.err = 0.1e-6;

###############################################################################
#                                 Rechnungen                                  #
###############################################################################

function y = plot_d(R, par)
	y = par(1) * R + par(2);
end

plot_x = c.data.val(:, 1);
plot_y = 1 ./ c.data.val(:, 2);
plot_error = 1 ./ c.data.val(:, 2).^2 * phi.err;

plot_data = [c.data.val plot_x plot_y plot_error];
save c.csv plot_data

[f, par, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		plot_x,
		plot_y,
		[1, 1],
		"plot_d",
		0.001,
		20,
		1./plot_error
		);

function_x = (min(plot_x) : (max(plot_x)-min(plot_x))/100 : max(plot_x))';
function_y = plot_d(function_x, par);

clf;
hold on;

p1 = errorbar(plot_x, plot_y, plot_error);
p2 = plot(function_x, function_y);

set(gca(), "fontsize", 20);
xlabel("R in [Ohm]");
ylabel("1 / phi");
set(p1, "linestyle", "none");
set(p1, "marker", "+");
title("Empfindlichkeit");

print("plot-empfindlichkeit.eps", "-tight");

c.alpha.val = par(1);
c.alpha.err = sqrt(diag(covp))(1);

c.Rg.val = par(2) / c.alpha.val;
c.Rg.err = sqrt(
(sqrt(diag(covp))(2) / c.alpha.val)^2
+ (par(2) / (c.alpha.val^2) * c.alpha.err)^2
);

c.cI.val =  (c.R1.val + c.R2.val) / (c.alpha.val * c.U0.val * c.R2.val);
c.cI.err = sqrt(
		((c.R1.val + c.R2.val) / (c.alpha.val^2 * c.U0.val * c.R2.val) * c.alpha.err)^2
		+ (1 / (c.alpha.val * c.U0.val * c.R2.val) * c.R1.err)^2
		+ ((c.alpha.val * c.U0.val * c.R2.val - (c.R1.val + c.R2.val) * c.alpha.val * c.U0.val) / (c.alpha.val^2 * c.U0.val^2 * c.R2.val^2) * c.R2.err)^2
		+ ((c.R1.val + c.R2.val) / (c.alpha.val * c.U0.val^2 * c.R2.val) * c.U0.err)^2
		);

printf("α = %.3g ± %.2g\n", c.alpha.val, c.alpha.err);
printf("R_g = %.3g ± %.2g\n", c.Rg.val, c.Rg.err);
printf("c_I = %.3g ± %.2g\n", c.cI.val, c.cI.err);

printf("\n");

###############################################################################
#                                  Aufgabe h                                  #
###############################################################################

disp("Aufgabe h")

function y = plot_h(t, par)
	y = par(1) - t / par(2);
end

plot_x = h.data.val(:, 1);
plot_y = log(h.data.val(:, 2));
plot_error = abs(1 ./ h.data.val(:, 2) * phi.err);

plot_data = [h.data.val plot_x plot_y plot_error];
save h.csv plot_data


[f, par, cvg, iter, corp, covp, covr, stdredid] = leasqr(
		plot_x,
		plot_y,
		[1, 1],
		"plot_h",
		0.001,
		20,
		1./plot_error
		);

function_x = (min(plot_x) : (max(plot_x)-min(plot_x))/10 : max(plot_x))';
function_y = plot_h(function_x, par);

clf;
hold on;

p1 = errorbar(plot_x, plot_y, plot_error);
p2 = plot(function_x, function_y);

set(gca(), "fontsize", 20);
xlabel("t in [s]");
ylabel("ln(phi)");
set(p1, "linestyle", "none");
set(p1, "marker", "+");
title("großer Widerstand");

print("plot-widerstand.eps", "-tight");

h.Q0.val = exp(par(1));
h.Q0.err = exp(par(1)) * par(1) * sqrt(diag(covp))(1);

h.RC.val = par(2);
h.RC.err = sqrt(diag(covp))(2);

h.R.val = h.RC.val / h.C.val;
h.R.err = sqrt(
		(1/h.C.val * h.RC.err)^2
		+ (h.RC.val/h.C.val^2 * h.C.err)^2
		);

printf("Q_0 = %.3g ± %.2g\n", h.Q0.val, h.Q0.err);
printf("RC = %.3g ± %.2g\n", h.RC.val, h.RC.err);
printf("R = %.3g ± %.2g\n", h.R.val, h.R.err);
