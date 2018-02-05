@echo off


cls

color 79

@ ECHO.

@ ECHO.

@ ECHO   =============Android渠道包测试=============

@ ECHO.  

@ ECHO   ===开始测试，请不要关闭本窗口===
=====
@ ECHO.

@ ECHO   =====================================

@ ECHO.  


monkeyrunner %~dp0SJApkTest.py


@ ECHO.

@ ECHO.

@ ECHO.

@ ECHO. 测试结束，结果存放在 ./Apk_Test/log 里。

echo. & pause > nul