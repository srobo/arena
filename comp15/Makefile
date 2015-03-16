
all: score-sheet-2015.pdf

%.pdf: %.svg
	inkscape -A $@ $<

clean:
	rm -f *.pdf
