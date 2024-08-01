echo off
set postTitle=%1
set currentDaytime=%time:~0,2%H%time:~3,2%M%time:~6,2%S
rem check if post name is provided
if "%1"=="" (
    echo need a argument as post title, using ctime as defalut
    set postTitle=%currentDaytime%
)


set currentDate=%date:~0,4%-%date:~5,2%-%date:~8,2%
set postFileName=%currentDate%-%postTitle%.md
echo %postFileName%
rem use jekyll compose to create a post
call bundle exec jekyll compose %postTitle%
rem get pwd
set currentDirectory=%cd%

rem get typora path
rem ###############################################################
rem ########### CHANGE THIS PATH TO YOUR OWN EDITOR PATH ##########
rem ###############################################################
set typoraPath="C:\Program Files\Typora\Typora.exe"


if not exist %typoraPath% (
    echo Typora not exist, no editor will be opened
    exit /b 1
)
rem get full path
set postFilePath=%currentDirectory%\_posts\%postFileName%

rem open blog by typora
start "" %typoraPath% %postFilePath%
exit /b 1