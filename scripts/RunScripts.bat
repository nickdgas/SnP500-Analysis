@echo off

echo Collecting raw data...
python scripts\UpdateRawData.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Building Date, Security, and Type tables...
start cmd /c "python scripts\Date.py && python scripts\Security.py && python scripts\Type.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Merging to create Volume and Corporate Actions tables...
start cmd /c "python scripts\Volume.py && python scripts\CorporateActions.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Merging to create Market table...
start cmd /c "python scripts\Market.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Procedure complete
goto END

:ERROR
echo An error occurred while generating model.
goto END

:END
