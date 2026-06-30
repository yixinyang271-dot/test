#!/bin/bash
echo "正在安装“布法罗”项目依赖..."
pip3 install requests vosk sounddevice pyserial
sudo apt-get install libportaudio2  # Linux音频驱动必要补丁
echo "安装完成。"