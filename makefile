# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

physik212-243-Martin.pdf: plot-empfindlichkeit.pdf plot-widerstand.pdf physik212-243-Martin.tex c.tex h.tex

%.tex: %.csv convert
	./convert $< > $@

c.csv h.csv plot-empfindlichkeit.eps: 243.m
	./243.m

%.pdf: %.eps
	epstopdf $<
