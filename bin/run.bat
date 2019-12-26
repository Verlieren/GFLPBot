@echo off
cls
:start
@python %~dp0\run %*
@echo.
@echo Restarting...
@echo.
goto start