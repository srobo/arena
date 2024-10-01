
all: score-sheet-2025.pdf

%.pdf: %.svg
	inkscape --export-filename colour-$@ $<
	gs -sOutputFile=$@ -sDEVICE=pdfwrite \
		-sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray \
		-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH colour-$@

clean:
	rm -f *.pdf
