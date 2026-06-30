import os
import sys
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import requests
import pyttsx3  # 新增：文字转语音库

# ================= 配置区 =================
MODEL_PATH = "vosk-model-small-cn"
LLM_API = "http://localhost:8080/v1/chat/completions"
WAKE_WORD = "布法罗"
FUZZY_WAKE_WORDS = [WAKE_WORD, "不法", "不法啰", "不啰", "布法", "不发"]


class BuffaloTester:
    def __init__(self):
        # 1. 初始化语音合成引擎（说话）
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # 说话速度
        self.engine.setProperty('volume', 1.0)  # 音量

        # 2. 初始化识别模型（听）
        if not os.path.exists(MODEL_PATH):
            print(f"错误：找不到模型文件夹 {MODEL_PATH}")
            sys.exit(1)
        self.model = Model(MODEL_PATH)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.q = queue.Queue()
        self.is_awake = False

    def speak(self, text):
        """让电脑开口说话"""
        print(f"【语音输出】: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def audio_callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def mock_hardware_send(self, action_name, v, w):
        print(f"\n⚡ [硬件执行] {action_name} | v:{v} w:{w}")
        # 在执行指令时，也播报一下
        self.speak(f"好的，开始{action_name}")

    def chat_with_ai(self, user_text):
        try:
            r = requests.post(LLM_API, json={"messages": [{"role": "user", "content": user_text}]}, timeout=1.5)
            return r.json()['choices'][0]['message']['content']
        except:
            return "收到，正在为您处理。"

    def start_test(self):
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self.audio_callback):
            print("\n>>> 【布法罗】已就绪，等待唤醒...")

            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result_dict = json.loads(self.rec.Result())
                    text = result_dict.get("text", "").replace(" ", "")

                    if not text: continue
                    print(f"【识别到文字】: {text}")

                    # 1. 唤醒
                    if not self.is_awake:
                        if any(word in text for word in FUZZY_WAKE_WORDS):
                            self.is_awake = True
                            self.speak("哎！我在呢。有什么吩咐？")
                        continue

                    # 2. 指令处理
                    if "前进" in text:
                        self.mock_hardware_send("前进", 0.5, 0.0)
                    elif "停" in text:
                        self.mock_hardware_send("停车", 0.0, 0.0)
                    elif "再见" in text:
                        self.is_awake = False
                        self.speak("好的，布法罗休息了。")
                    else:
                        # 3. 聊天
                        reply = self.chat_with_ai(text)
                        self.speak(reply)


if __name__ == "__main__":
    tester = BuffaloTester()
    tester.start_test()