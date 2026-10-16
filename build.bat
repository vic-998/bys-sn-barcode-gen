@echo off
chcp 65001 >nul
echo ============================================
echo   SN 条码生成器 - 打包为 EXE
echo ============================================
echo.

python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [错误] 依赖安装失败
  pause
  exit /b 1
)

echo.
echo 开始打包（首次打包可能需要几分钟）...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name sn-barcode-gen ^
  --icon icon.ico ^
  --add-data "templates;templates" ^
  --collect-all barcode ^
  app.py

if errorlevel 1 (
  echo [错误] 打包失败
  pause
  exit /b 1
)

echo.
echo ============================================
echo   打包完成！exe 位于 dist\sn-barcode-gen.exe
echo   双击运行会自动打开浏览器
echo ============================================
pause
