
# 傳統冷氣大變身
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

本專案接線嚴格參照 Raspberry Pi BCM 編碼，詳細接線表如下：

### 3.1 Raspberry Pi GPIO 配置表
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
[請在此處插入終端機執行成功的截圖]

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
