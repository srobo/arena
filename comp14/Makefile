all: method.pdf floor-protection-method.pdf

%.pdf: %.md
	pandoc -o $@ $^

.PHONY: clean

clean:
	-rm -f {method,floor-protection-method}.pdf
