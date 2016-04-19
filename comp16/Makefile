
all: score-sheet-2016.pdf flyer.pdf

%.pdf: %.svg
	inkscape -A colour-$@ $<
	gs -sOutputFile=$@ -sDEVICE=pdfwrite \
		-sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray \
		-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH colour-$@

flyer.pdf: flyer.svg
	inkscape -A $@ $<

clean:
	rm -f *.pdf
