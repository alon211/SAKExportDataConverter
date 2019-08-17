@echo off

title demo

call %cd%\venv\Scripts\activate.bat

python %cd%\gui.py 
call deactivate.bat
pause


