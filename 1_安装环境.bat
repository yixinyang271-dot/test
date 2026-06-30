@echo off
echo 正在为“布法罗”项目安装必要的 Python 模拟工具...
pip install requests vosk sounddevice pyserial
echo.
echo [成功] 环境安装完毕，请确保 vosk-model-small-cn 文件夹已放入当前目录。
pause