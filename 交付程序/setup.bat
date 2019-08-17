@echo off
echo "start check requirements.txt file"
if exist %cd%\requirements.txt (
   echo "check requirements.txt finish"
) else (
  echo "not exist requirements.txt"
)  
echo "start init env"
SET curdir=%cd%\venv
echo %curdir%
if exist  %curdir% (
 RD /S /q %cd%\venv
 echo "delete old  venv"
 TIMEOUT /T 8
 echo "start create new venv"
 python -m venv ./venv
 TIMEOUT /T 5
 echo "create new venv finish"
) else (
 python -m venv ./venv
 echo "finish create venv"
)
 TIMEOUT /T 5
call %cd%\venv\Scripts\activate.bat
echo "source env finish"
echo "pwd is : %cd%"
TIMEOUT /T 5
pip install --no-index --ignore-installed  --find-links=whls -r requirements.txt
echo "install packages flowing:"
pip list
deactivate
echo "exit env virtual"
echo "wait 10 seconds...."
TIMEOUT /T 5
python -m %cd%\fit_env_dir.py
echo "pyhton3 fit envdir finish"
TIMEOUT /T 10
pause