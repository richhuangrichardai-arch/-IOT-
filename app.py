# -*- coding: utf-8 -*-
# 檔案名稱: app.py
# 專案名稱: SmartTempController
# 開發者: s11345024
# 描述: 基於 Flask 的樹莓派冷氣控制後端，負責接收網頁請求並控制 GPIO

from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# --- 硬體配置設定 ---
# 使用 BCM 晶片編號模式
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 定義 GPIO 腳位 (根據你的接線說明)
# PIN 11 -> GPIO 17 (灰色線) -> 繼電器1 -> 溫度下降
PIN_TEMP_DOWN = 17 
# PIN 13 -> GPIO 27 (白色線) -> 繼電器2 -> 溫度上升
PIN_TEMP_UP = 27
# PIN 15 -> GPIO 22 (紫色線) -> 繼電器3 -> 電源開/關
PIN_POWER = 22

# 初始化 GPIO 狀態
# 繼電器通常是低電位觸發(Low Trigger)或高電位觸發。
# 這裡預設為 HIGH (不動作)，當需要點擊時拉 LOW，再回覆 HIGH。
# 若你的繼電器是高電位觸發，請反過來設定。
pins = [PIN_TEMP_DOWN, PIN_TEMP_UP, PIN_POWER]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH) # 預設不導通

# --- 動作函式 ---
def press_button(pin):
    """
    模擬按下按鈕的動作：導通 -> 等待 0.5 秒 -> 斷開
    """
    try:
        print(f"Triggering Pin {pin}...")
        GPIO.output(pin, GPIO.LOW)  # 導通 (模擬按下)
        time.sleep(0.5)             # 持續按壓時間
        GPIO.output(pin, GPIO.HIGH) # 斷開 (模擬放開)
        return True
    except Exception as e:
        print(f"Error controlling GPIO: {e}")
        return False

# --- 網頁路由 ---

@app.route('/')
def index():
    """ 顯示控制主畫面 """
    return render_template('index.html')

@app.route('/control/<action>', methods=['POST'])
def control(action):
    """ 接收前端指令並執行對應的 GPIO 動作 """
    success = False
    message = ""

    if action == 'power':
        success = press_button(PIN_POWER)
        message = "冷氣電源已切換"
    elif action == 'up':
        success = press_button(PIN_TEMP_UP)
        message = "溫度已調升"
    elif action == 'down':
        success = press_button(PIN_TEMP_DOWN)
        message = "溫度已調降"
    else:
        message = "無效的指令"

    if success:
        return jsonify({'status': 'success', 'message': message})
    else:
        return jsonify({'status': 'error', 'message': 'GPIO 控制失敗'})

if __name__ == '__main__':
    # 監聽所有介面，Port 5000
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup() # 程式結束時清理 GPIO 設定