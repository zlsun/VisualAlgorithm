#!/usr/bin/env bash
rm -rf dist/
pyinstaller src/main_window.pyw -i src/icons/icon.ico --onefile --noconsole
ln -s src/examples/ dist/examples/
ln -s src/icons/    dist/icons/

