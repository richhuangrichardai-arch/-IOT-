# 傳統冷氣大變身
運用IOT的實作，實現傳統冷氣可以被遠端開關冷氣及調整溫度

<img width="480" height="800" alt="image" src="https://github.com/user-attachments/assets/96d4f7ea-b905-4c80-8235-599f78419d5e" />

# 📝 SmartTempController (Raspberry Pi IoT AC Remote)

**SmartTempController** 是一個充滿「生活溫度」（但實際是為了降溫 🧊）的物聯網專案。透過 Raspberry Pi 4 結合繼電器模組，將傳統紅外線冷氣遙控器升級為智慧家電，解決台灣夏日酷暑的生活痛點。

![Status](https://img.shields.io/badge/Status-Stable-success)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%204-C51A4A?logo=raspberry-pi)
![Language](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)

## 📖 目錄
1. [專案背景與發想情境](#1-專案背景與發想情境-motivation)
2. [硬體規格與組件](#2-硬體規格與組件)
3. [硬體介面詳細定義 (Pin Definitions)](#3-硬體介面詳細定義-pin-definitions)
    - [3.1 Raspberry Pi GPIO 配置表](#31-raspberry-pi-gpio-配置表)
    - [3.2 4路繼電器模組接腳定義](#32-4路繼電器模組接腳定義)
    - [3.3 遙控器改裝接線定義](#33-遙控器改裝接線定義)
4. [系統安裝與執行](#4-系統安裝與執行)
5. [軟體架構說明](#5-軟體架構說明)

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
| **主控制器** | [請在此處插入 Raspberry Pi 4 圖片] | **Raspberry Pi 4 Model B**<br>- CPU: BCM2711<br>- GPIO: 40-pin Header | 系統大腦，運行 Flask Web Server |
| **繼電器模組** | [請在此處插入繼電器圖片] | **Songle SRD-5VDC-SL-C** (4路)<br>- 觸發模式: **High Level Trigger**<br>- 接點: COM / NO | 模擬手指按壓動作 (電子開關) |
| **遙控器** | [請在此處插入遙控器圖片] | **DA-ARC-10** (改裝)<br>- 電壓: DC 3V<br>- 改裝: 焊接引出線至按鍵接點 | 發射紅外線訊號控制冷氣 |
| **連接元件** | - | 杜邦線、麵包板 | 訊號與電源分配 |

---

## 3. 硬體介面詳細定義 (Pin Definitions)

本專案接線嚴格參照 Raspberry Pi BCM 編碼與物理針腳對應，詳細接線表如下：

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

#### 輸入端 (控制側)
| 腳位標籤 | 說明 | 連接來源 (From) |
| :--- | :--- | :--- |
| **VCC** | 模組供電 (5V) | 麵包板 (+) 軌 |
| **GND** | 接地 (0V) | 麵包板 (-) 軌 |
| **IN1** | 通道 1 訊號 | RPi GPIO 17 (Pin 11) |
| **IN2** | 通道 2 訊號 | RPi GPIO 27 (Pin 13) |
| **IN3** | 通道 3 訊號 | RPi GPIO 22 (Pin 15) |

#### 輸出端 (負載側 - 乾接點模式)
輸出端採用 **NO (Normally Open, 常開)** 接法，模擬按鈕按下時導通。

| 繼電器通道 | 端子接法 | 連接線色 | 連接目標 (To) | 動作邏輯 |
| :--- | :--- | :---: | :--- | :--- |
| **Relay 1** | **COM** (中) + **NO** (下) | ⚫ 黑色 x2 | 遙控器 **[Temp Down]** 焊點 | High -> 導通 (降溫) |
| **Relay 2** | **COM** (中) + **NO** (下) | ⚪ 白色 x2 | 遙控器 **[Temp Up]** 焊點 | High -> 導通 (升溫) |
| **Relay 3** | **COM** (中) + **NO** (下) | 🟣 紫色 x2 | 遙控器 **[Power]** 焊點 | High -> 導通 (開關) |

> ⚠️ **注意**：繼電器上的 NC (常閉) 端子請保持懸空，切勿接線，否則會造成按鈕長按卡死。

### 3.3 遙控器改裝接線定義
遙控器拆解後，針對 PCB 板上的碳膜按鍵進行引線焊接。

| 按鍵功能 | 改裝方式 | 對應繼電器 | 觸發後行為 |
| :--- | :--- | :---: | :--- |
| **溫度 (-)** | 焊接兩條引線至按鍵接觸點兩端 | Relay 1 | 發射 IR 降溫訊號 |
| **溫度 (+)** | 焊接兩條引線至按鍵接觸點兩端 | Relay 2 | 發射 IR 升溫訊號 |
| **電源 (Power)** | 焊接兩條引線至按鍵接觸點兩端 | Relay 3 | 發射 IR 開/關訊號 |

---

## 4. 系統安裝與執行

本專案運行於 Raspberry Pi OS (Buster/Legacy)，使用 Python 虛擬環境部署。

### 1. 環境初始化 (首次安裝)
```bash
# 更新系統軟體源 (Legacy 專用)
sudo sed -i 's|[http://raspbian.raspberrypi.org/raspbian](http://raspbian.raspberrypi.org/raspbian)|[http://legacy.raspbian.org/raspbian](http://legacy.raspbian.org/raspbian)|g' /etc/apt/sources.list
sudo apt-get -o Acquire::Check-Valid-Until=false update --allow-releaseinfo-change

# 安裝系統工具
sudo apt-get install python3-venv python3-pip -y
