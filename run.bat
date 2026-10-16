@echo off
chcp 65001 >nul
python -m pip install -r requirements.txt
echo 启动中... 浏览器将自动打开 http://127.0.0.1:5000
python app.py
pause
