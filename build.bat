rd /S /Q dist
pyinstaller src\main_window.pyw -i src\icons\icon.ico --onefile --noconsole
mklink /J dist\examples\ src\examples\
mklink /J dist\icons\    src\icons\