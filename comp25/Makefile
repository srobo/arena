
all: score-sheet-2025.pdf score-sheet-2025.png

%.png: %.pdf
	pdftoppm $< -png > $@

%.pdf: %.svg
	inkscape --export-filename colour-$@ $<
	gs -sOutputFile=$@ -sDEVICE=pdfwrite \
		-sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray \
		-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH colour-$@

clean:
	rm -f *.pdf *.png
