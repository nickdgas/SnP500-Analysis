@echo off

echo Collecting raw data...
python scripts\UpdateRawData.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Building Date, Security, and Type tables...
start cmd /c "python scripts\Date.py && python scripts\Security.py && python scripts\Type.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Establishing relationships for Market and Corporate Actions...
start cmd /c "python scripts\Volume.py && python scripts\CorporateActions.py && python scripts\Market.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Relational model completed successfully!
goto END

:ERROR
echo An error occurred while generating model.
goto END

:END
