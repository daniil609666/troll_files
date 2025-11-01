@echo off 
setlocal enabledelayedexpansion 
color 17 
for /l %%n in (0, 1, 100) do ( 
set /a rand=!random! %% 9 
set /a rand2=!random! %% 9 
start cmd /k "@echo off && color 2 && title Hacking... && dir C:\ /s"
set /a randTimer=!random! %% 5+1 
timeout /t !randTimer! /nobreak >nul 
) 
pause 
