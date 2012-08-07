# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

physik212-249-Martin.pdf: physik212-249-Martin.tex luft.pdf fadenstrahl.pdf
	latexmk -pdf $<

%.pdf: %.eps
	epstopdf $<

luft.eps fadenstrahl.eps: 249.m
	./$<

.PHONY: clean
clean:
	$(RM) luft.eps
	$(RM) luft.pdf
	latexmk -C
