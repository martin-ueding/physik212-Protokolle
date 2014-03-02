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

# Set output to a nice PDF.
set terminal postscript eps enhanced color solid defaultplex "Helvetica" 12
set output "|epstopdf --filter > cunningham-gnuplot.pdf"

f(x) = a + b * x

fit f(x) "./cunningham.txt" using 1:2:4 via a,b

set xrange [0:4e6]

set xlabel "1/r / [1/m]"
set ylabel "e_S^{2/3} / [C^{2/3}]"
plot "./cunningham.txt" with xyerrorbars, f(x)

set output
