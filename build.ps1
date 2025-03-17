# 设置控制台编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "系统工具箱打包工具"

Write-Host "[信息] 正在清理旧的构建文件..." -ForegroundColor Green

# 创建必要的目录
if (-not (Test-Path "output")) {
    New-Item -ItemType Directory -Path "output" | Out-Null
}

# 清理旧的构建文件
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force
}
if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force
}

Write-Host "[信息] 正在使用 PyInstaller 打包..." -ForegroundColor Green
python -m PyInstaller system_toolbox.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] PyInstaller 打包失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "[信息] 正在使用 Inno Setup 创建安装程序..." -ForegroundColor Green
$innoSetupPath = "D:\Inno Setup 6\ISCC.exe"

if (Test-Path $innoSetupPath) {
    & $innoSetupPath /Q "setup.iss"
} else {
    Write-Host "[错误] 未找到 Inno Setup，请确保已安装 Inno Setup 6" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] Inno Setup 打包失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "[信息] 构建完成！" -ForegroundColor Green
Write-Host "[信息] 安装程序位于 output 目录中" -ForegroundColor Green
Write-Host ""

Get-ChildItem -Path "output" -Filter "*.exe" | ForEach-Object { $_.Name }
Write-Host ""
Read-Host "按回车键退出" 