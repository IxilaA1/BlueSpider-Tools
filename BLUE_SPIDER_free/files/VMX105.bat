@echo off
color 0D
setlocal EnableDelayedExpansion

echo.
echo === System Information Collection and Display ===
echo.

echo 1.
set /p USER_IP="Enter an IPv4 address: "
echo Entered IP address: %USER_IP%
echo.

echo 2.
echo Computer Name: %COMPUTERNAME%
echo.

echo 3.
echo List of Users:
powershell -Command "Get-LocalUser | Select-Object -ExpandProperty Name"
echo.

pause
endlocal
