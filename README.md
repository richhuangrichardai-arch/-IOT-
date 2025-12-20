# 影片 https://youtube.com/shorts/i6UyL6o8F80?feature=share
# 傳統冷氣大變身
# 作者：113453024 黃子男
運用IOT的實作，實現傳統冷氣可以被遠端開關冷氣及調整溫度
<img width="480" height="800" alt="image" src="https://github.com/user-attachments/assets/96d4f7ea-b905-4c80-8235-599f78419d5e" />

# 📝 SmartTempController (Raspberry Pi IoT AC Remote)

**SmartTempController** 是一個充滿「生活溫度」（但實際是為了降溫 🧊）的物聯網專案。透過 Raspberry Pi 4 結合繼電器模組，將傳統紅外線冷氣遙控器升級為智慧家電，解決台灣夏日酷暑的生活痛點。

![Status](https://img.shields.io/badge/Status-Stable-success)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%204-C51A4A?logo=raspberry-pi)
![Language](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Framework](https://img.shields.io/badge/Framework-Flask-green?logo=flask)

## 📖 目錄
1. [專案背景與發想情境](#1-專案背景與發想情境-motivation)
2. [硬體規格與組件](#2-硬體規格與組件)
3. [硬體介面詳細定義](#3-硬體介面詳細定義-pin-definitions)
4. [系統部署與安裝](#4-系統部署與安裝-deployment)
5. [啟動服務說明](#5-啟動服務說明-startup)
6. [軟體架構解析](#6-軟體架構解析-architecture)

---

## 1. 專案背景與發想情境 (Motivation)

### 🥵 修改前：身心俱疲的「大烤箱」體驗
生活在台灣的我們都深有體會，夏天的太陽毒辣得讓人無處可逃。試想一下這樣的場景：
當你結束了一整天繁忙的工作，拖著疲憊的身軀回到家，渴望的是一個可以放鬆的避風港。然而，打開房門的那一剎那，迎接你的不是舒適，而是一股撲面而來的熱浪。經過整日曝曬的房間，就像一個**高溫悶熱的「大烤箱」**。

即使你用最快速度抓起遙控器打開冷氣，接下來的 15 分鐘，你依然要在悶熱的空氣中揮汗如雨，等待室溫慢慢下降。那一刻，**身體是黏膩不適的，心理是煩躁崩潰的**，回家的放鬆感蕩然無存。

### 🥶 修改後：一進門的「幸福涼感」
這就是 **SmartTempController** 誕生的初衷！
既然家裡的舊冷氣不支援聯網，我就用樹莓派自己打造。現在的情境完全改變了：
在下班回家的路上，我只需要拿出手機，連上自己寫的網頁，輕輕按下「電源開啟」。

當我再次轉動家門鑰匙，推開門的那一瞬間，**一陣涼爽的冷空氣迎面而來**。不再有悶熱與煩躁，取而代之的是**身體瞬間的舒爽與心理的療癒**。這不只是一個遠端開關，它是將「痛苦的等待」轉化為「即時享受」的幸福感來源。

---

## 2. 硬體規格與組件

| 項目 | 圖片 | 型號/規格 | 用途 |
| :--- | :---: | :--- | :--- |
| **主控制器** | [請在此處插入 Raspberry Pi 圖片] | **Raspberry Pi 4 Model B**<br>- CPU: BCM2711<br>- GPIO: 40-pin Header | 系統大腦，運行 Flask Web Server |
| **繼電器模組** | [請在此處插入繼電器圖片] | **Songle SRD-5VDC-SL-C** (4路)<br>- 觸發模式: **High Level Trigger**<br>- 接點: COM / NO | 模擬手指按壓動作 (電子開關) |
| **遙控器** | [請在此處插入遙控器圖片] | **DA-ARC-10** (改裝)<br>- 電壓: DC 3V<br>- 改裝: 焊接引出線至按鍵接點 | 發射紅外線訊號控制冷氣 |

---

## 3. 硬體介面詳細定義 (Pin Definitions)
<img width="480" height="800" alt="image" src="https://github.com/user-attachments/assets/1d424bd6-6bc3-44c8-a923-7991ec70c7dc" />
本專案接線嚴格參照 Raspberry Pi BCM 編碼，詳細接線表如下：

### 3.1 Raspberry Pi GPIO 配置表
<img width="480" height="800" alt="image" src="https://github.com/user-attachments/assets/2066e02c-9508-4ed8-9011-2f4a39d684e2" />

| 實體針腳 (Physical Pin) | BCM 編碼 | 線材顏色 | 連接目標 | 功能描述 |
| :---: | :---: | :---: | :--- | :--- |
| **04** | - | 🔴 紅色 | 麵包板 (+) 軌 | 供應繼電器模組 **5V 電源** |
| **06** | - | ⚫ 黑色 | 麵包板 (-) 軌 | 系統 **GND 接地** |
| **11** | **GPIO 17** | 🔘 灰色 | Relay IN1 | 控制 **「溫度調降」** |
| **13** | **GPIO 27** | ⚪ 白色 | Relay IN2 | 控制 **「溫度調升」** |
| **15** | **GPIO 22** | 🟣 紫色 | Relay IN3 | 控制 **「電源開/關」** |

### 3.2 4路繼電器模組接腳定義
本專案使用 Songle 5V 繼電器，跳線帽 (Jumper) 設定為 **High Level Trigger (高電位觸發)**。

| 繼電器通道 | 端子接法 (Output) | 連接線色 | 連接目標 (To) | 動作邏輯 |
| :--- | :--- | :---: | :--- | :--- |
| **Relay 1** | **COM** (中) + **NO** (下) | ⚫ 黑色 x2 | 遙控器 **[Temp Down]** | High -> 導通 (降溫) |
| **Relay 2** | **COM** (中) + **NO** (下) | ⚪ 白色 x2 | 遙控器 **[Temp Up]** | High -> 導通 (升溫) |
| **Relay 3** | **COM** (中) + **NO** (下) | 🟣 紫色 x2 | 遙控器 **[Power]** | High -> 導通 (開關) |

> ⚠️ **注意**：繼電器上的 NC (常閉) 端子請保持懸空，切勿接線。

### 3.2.5搖控器
<img width="480" height="800" alt="image" src="https://github.com/user-attachments/assets/748fcdc9-8883-4310-9e05-26b34e8369f6" />
### 3.2.6實體接線圖
<img width="683" height="907" alt="image" src="https://github.com/user-attachments/assets/77c2bec9-692e-401e-a73a-c82bea4d53bd" />
### 3.2.7線路示意圖
<img width="480" height="800" alt="image" src="https://github.com/user-attachments/assets/b024fde6-e652-4b13-8a98-33170127d39d" />

---

## 4. 系統部署與安裝 (Deployment)

本專案運行於 **Raspberry Pi OS (Legacy Buster)** 環境，建議使用 Python 虛擬環境進行部署以保持系統潔淨。

### Step 1: 系統環境修復 (針對 Legacy OS)
由於 Buster 版本源已封存，需先執行以下指令修復 `sources.list`：

```bash
# 1. 切換至 Legacy 軟體源
sudo sed -i 's|http://raspbian.raspberrypi.org/raspbian|http://legacy.raspbian.org/raspbian|g' /etc/apt/sources.list

# 2. 更新系統清單 (忽略過期時間檢查)
sudo apt-get -o Acquire::Check-Valid-Until=false update --allow-releaseinfo-change

# 3. 安裝虛擬環境工具
sudo apt-get install python3-venv python3-pip -y
```

### Step 2: 建立專案環境

```bash
# 1. 建立專案目錄
mkdir -p /home/g11345024/smart_ac
cd /home/g11345024/smart_ac

# 2. 建立 Python 虛擬環境 (venv)
python3 -m venv venv

# 3. 啟用虛擬環境
source venv/bin/activate

# 4. 安裝相依套件 (Flask, GPIO)
pip install Flask RPi.GPIO
```

---

## 5. 啟動服務說明 (Startup)

完成部署後，請依照以下步驟啟動冷氣控制服務。

### 🚀 啟動指令
由於需要存取 GPIO 硬體針腳，必須使用 `sudo` 權限執行，並指向虛擬環境內的 Python 直譯器：

```bash
cd /home/g11345024/smart_ac
sudo ./venv/bin/python app.py
```

### ✅ 成功畫面確認
當終端機出現以下訊息時，代表服務已正常運作：
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.137.186:5000
```
<img width="565" height="687" alt="image" src="https://github.com/user-attachments/assets/c205a345-a63c-4d9a-8205-3d83414c3ef3" />

### 📱 使用者操作
1.  拿出手機或電腦，連接至與樹莓派相同的 Wi-Fi。
2.  開啟瀏覽器，輸入網址：`http://192.168.137.186:5000`
3.  進入 **「智慧冷氣中控」** 介面進行操作。

---

## 6. 軟體架構解析 (Architecture)

本系統採用 **MVC (Model-View-Controller)** 概念設計，基於 Python Flask 輕量級框架。

### 📂 專案目錄結構
```text
/home/g11345024/smart_ac/
├── app.py                # 核心控制器 (Controller & GPIO Logic)
├── venv/                 # Python 虛擬環境 (System Env)
├── templates/
│   └── index.html        # 前端操作介面 (View)
└── static/
    └── style.css         # 介面視覺樣式 (Style)
```

### 🧩 模組功能職責

#### 1. `app.py` (核心邏輯)
* **GPIO 初始化**：
    * 設定模式為 `BCM`。
    * **關鍵安全設定**：啟動時將所有 GPIO 輸出設為 `LOW` (0V)，確保繼電器保持**斷開**狀態，防止誤觸發。
* **Web 路由 (Routes)**：
    * `GET /` : 渲染操作介面。
    * `POST /control/<action>` : 接收前端指令 (up/down/power)。
* **硬體驅動 (Driver)**：
    * `press_button(pin)` : 執行「輸出 HIGH -> 等待 0.5秒 -> 輸出 LOW」的完整按壓模擬流程。

#### 2. `templates/index.html` (前端介面)
* **RWD 響應式設計**：確保在手機與桌面端皆有良好的操作體驗。
* **AJAX 非同步通訊**：使用 JavaScript `fetch` API 發送指令，操作時**頁面不需刷新**，體驗流暢。
* **SweetAlert2**：整合第三方函式庫，提供美觀的操作回饋 (Success/Error 彈窗)。

#### 3. `static/style.css` (視覺設計)
* **現代化 UI**：使用漸層色 (Gradient) 按鈕與卡片式 (Card) 佈局。
* **互動回饋**：按鈕具備點擊縮放動畫 (`transform: scale`)，提升操作手感。

---

## 7. 關鍵程式碼說明 (Code Analysis)

本章節解析 `app.py` 中控制硬體的核心邏輯，說明如何確保繼電器動作符合預期。

### 7.1 安全初始化 (Safety Initialization)
為防止系統一上電就誤觸發繼電器（導致冷氣被誤開），我們在程式啟動時強制將 GPIO 拉低。

```python
# app.py 片段
pins = [PIN_TEMP_DOWN, PIN_TEMP_UP, PIN_POWER]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    # ⚠️ 關鍵：預設輸出 LOW (0V)
    # 因為繼電器設為 High Trigger，所以 LOW 代表「斷開/不動作」
    GPIO.output(pin, GPIO.LOW)
```

### 7.2 按鈕動作模擬 (Button Simulation)
為了模擬真實的手指按壓行為，我們不能讓 GPIO 一直保持 High，必須在短暫導通後斷開，形成一個 **脈衝 (Pulse)**。

```python
def press_button(pin):
    try:
        # 1. 導通繼電器 (模擬手指按下)
        GPIO.output(pin, GPIO.HIGH)
        
        # 2. 暫停 0.5 秒 (模擬按壓持續時間)
        time.sleep(0.5)
        
        # 3. 斷開繼電器 (模擬手指放開)
        GPIO.output(pin, GPIO.LOW)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
```
> **邏輯解析**：
> * `GPIO.HIGH`：繼電器線圈通電，COM 與 NO 導通 -> 遙控器發射訊號。
> * `time.sleep(0.5)`：若時間太短，遙控器IC可能偵測不到；若太長，會變成「長按」。0.5秒是最佳經驗值。
> * `GPIO.LOW`：恢復待機狀態，準備下一次操作。

### 7.3 Web 路由映射 (Route Mapping)
前端網頁透過 AJAX 發送字串指令，後端透過字典或條件判斷來映射到具體的 GPIO 腳位。

```python
@app.route('/control/<action>', methods=['POST'])
def control(action):
    # 根據網址中的 action 參數決定觸發哪個腳位
    if action == 'power':
        success = press_button(PIN_POWER)      # GPIO 22
    elif action == 'up':
        success = press_button(PIN_TEMP_UP)    # GPIO 27
    elif action == 'down':
        success = press_button(PIN_TEMP_DOWN)  # GPIO 17
    
    # 回傳 JSON 格式讓前端 SweetAlert 顯示結果
    if success:
        return jsonify({'status': 'success', 'message': '指令發送成功'})
```

---

## 8. 程式開發注意事項 (Precautions)

在實作與測試過程中，以下幾點是確保系統穩定與硬體安全的關鍵：

### ⚠️ 硬體安全
1.  **繼電器觸發模式確認**：
    * 本程式是針對 **High Level Trigger (高電位觸發)** 撰寫。
    * 務必檢查繼電器模組上的 **黃色跳線帽 (Jumper)** 是否插在 **H** 的位置。
    * 若插在 L (Low)，程式邏輯需全部反轉（LOW變導通），否則會一開機就全開。
2.  **NC 端子懸空**：
    * 繼電器輸出端的 **NC (常閉)** 腳位絕對不能接線。若誤接，冷氣遙控器會被判定為「按鈕一直被按著」，導致遙控器當機或電池耗盡。

### ⚠️ 系統權限
1.  **Sudo 權限要求**：
    * `RPi.GPIO` 函式庫需要存取 `/dev/gpiomem` 或 `/dev/mem`，這通常需要 root 權限。
    * 執行程式時必須加上 `sudo`，例如：`sudo ./venv/bin/python app.py`。
    * 若直接用 IDE (如 Thonny) 執行，需確認 IDE 是否以 root 權限開啟。

### ⚠️ 網路連線
1.  **固定 IP 設定**：
    * 建議將樹莓派設定為固定 IP (Static IP)，以免路由器重啟後 IP 跑掉，導致手機網頁連不上。
    * 目前的程式預設監聽 `0.0.0.0`，代表接受區網內所有裝置的連線，這是正確的設定。
