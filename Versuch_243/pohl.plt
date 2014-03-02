#!/usr/bin/gnuplot -p
# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

###############################################################################
#                                   License                                   #
###############################################################################
#
# This gnuplot script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option) any
# later version.
#
# This is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this. If not, see <http://www.gnu.org/licenses/>.

set encoding utf8

###############################################################################
#                                    106.c                                    #
###############################################################################

# Set output to a nice PDF.
set terminal postscript eps enhanced color solid defaultplex "Helvetica" 12
set output "|epstopdf --filter > plot_c.pdf"

# Label the axes.
set xlabel "Endladungsdauer"
set ylabel "Maximalamplitude"

# Enable the grid.
set grid

# Set the title of the whole graph.
set title "physik212 Versuch 243: Aufgabe 106.h"

f1(x) = a * exp(-x/g);

fit f1(x) "test.dat" using 1:2:3 via a,g

set logscale y

# Plot the data with the fit.
plot "test.dat" with yerrorbars lc rgb "#000000" title "Daten", \
	 f1(x) lc rgb "#000000" title "Fit"

# Set the output again so that the PDF is really written to.
set output
