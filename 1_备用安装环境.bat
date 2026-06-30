@echo off
echo ==================================================
echo   正在为“布法罗”智慧轮椅项目安装 AI 依赖包...
echo ==================================================
echo.

:: 使用清华大学镜像源加速下载，防止网络卡顿
pip install requests vosk sounddevice pyserial -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ==================================================
echo   安装尝试完成！
echo   如果上面没有出现红色的 ERROR，说明安装成功。
echo ==================================================
pause