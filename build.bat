@echo off
rd /S /Q dist
C:\bin\Python34\Scripts\pyinstaller src\main_window.pyw -i src\icons\icon.ico --onefile --noconsole
mklink /J dist\examples\ src\examples\
mklink /J dist\icons\    src\icons\
