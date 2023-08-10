echo off
@REM 当前文件夹路径
set Root=%~dp0
@REM 拖入的文件
set DropFile=%~1
@REM 导出路径
set Output=%Root%output
python %Root%/src/main.py %DropFile% %Output%
pause