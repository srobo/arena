
all: score-sheet-2015.pdf arena-label-A.pdf arena-label-B.pdf

%.pdf: %.svg
	inkscape -A colour-$@ $<
	gs -sOutputFile=$@ -sDEVICE=pdfwrite \
		-sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray \
		-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH colour-$@

clean:
	rm -f *.pdf
