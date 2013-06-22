# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

physik212-248-Martin.pdf: hysterese.pdf hysterese-mua.pdf hysterese-1000.pdf

%.pdf: %.tex
	latexmk -pdf $<

%.pdf: %.eps
	epstopdf $<

hysterese.eps: 248.m
	./$<
