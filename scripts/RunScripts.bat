@echo off

echo Collecting raw data...
python scripts\UpdateRawData.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Building relational model...
start cmd /c "python scripts\Date.py && python scripts\Security.py && python scripts\Type.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Establishing relationships...
python scripts\Market.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Relational model completed successfully!
goto END

:ERROR
echo An error occurred while generating model.
goto END

:END
