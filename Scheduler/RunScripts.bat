@echo off

echo Running script1.py...
python script1.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Running scripts 2, 3, and 4...
start cmd /c "python script2.py && python script3.py && python script4.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Running script5.py...
python script5.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo All scripts completed successfully!
goto END

:ERROR
echo An error occurred while running the scripts.
goto END

:END
