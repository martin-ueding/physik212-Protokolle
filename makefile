# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

physik212-249-Martin.pdf: physik212-249-Martin.tex luft.pdf
	latexmk -pdf $<

%.pdf: %.eps
	epstopdf $<

luft.eps: 249.m
	./$<

.PHONY: clean
clean:
	$(RM) *.class *.jar
	$(RM) *.o *.out
	$(RM) *.pyc *.pyo
	$(RM) *.orig
