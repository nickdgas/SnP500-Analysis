@echo off

echo Collecting raw data...
python Raw\UpdateRawData.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Building relational model...
start cmd /c "python Date\Date.py && python Security\Security.py && python Type\Type.py"
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Establishing relationships...
python Market\Market.py
if %ERRORLEVEL% NEQ 0 goto ERROR

echo Relational model completed successfully!
goto END

:ERROR
echo An error occurred while generating model.
goto END

:END
