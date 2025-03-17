@echo off
chcp 65001
title 系统工具箱打包工具

rem 创建必要的目录
if not exist "output" mkdir output

echo [信息] 正在清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo [信息] 正在使用 PyInstaller 打包...
py -m PyInstaller system_toolbox.spec

if errorlevel 1 (
    echo [错误] PyInstaller 打包失败
    pause
    exit /b 1
)

echo [信息] 正在使用 Inno Setup 创建安装程序...
if exist "D:\Inno Setup 6\ISCC.exe" (
    "D:\Inno Setup 6\ISCC.exe" /Q "setup.iss"
) else (
    echo [错误] 未找到 Inno Setup，请确保已安装 Inno Setup 6
    pause
    exit /b 1
)

if errorlevel 1 (
    echo [错误] Inno Setup 打包失败
    pause
    exit /b 1
)

echo [信息] 构建完成！
echo [信息] 安装程序位于 output 目录中
echo.
dir /b "output\*.exe"
echo.
pause 