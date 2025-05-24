@echo off
echo.
echo.
echo.
echo ===============================================================
echo Building for Windows...
echo ===============================================================
echo.
echo.
echo.
pyinstaller --onefile --noconsole --optimize=2 clusterifier.py
echo.
echo.
echo.
echo ===============================================================
echo Building for Linux...
echo ===============================================================
echo.
echo.
echo.
wsl pyinstaller --onefile --noconsole --optimize=2 clusterifier.py
echo.
echo.
echo.
echo ===============================================================
echo Done!
echo ===============================================================
pause