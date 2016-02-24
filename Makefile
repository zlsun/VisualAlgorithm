
.PHONY: all clean run dist wc

all: run

clean:
	@rm -rf dist/

run:
	@cd src && ./main_window.pyw

dist: clean
	pyinstaller src/main_window.pyw -i src/icons/icon.ico --onefile --noconsole
	ln -s src/examples/ dist/examples/
	ln -s src/icons/    dist/icons/

wc:
	@echo "Lines|Words|Bytes|File"
	@echo "================================================"
	@wc src/*.py{,w} src/*/*.py

