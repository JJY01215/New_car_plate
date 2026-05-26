# 📊 基於深度學習之高強韌性智慧校園車牌辨識與門禁控制系統

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework-EasyOCR](https://img.shields.io/badge/Framework-EasyOCR-orange.svg)](https://github.com/JaidedAI/EasyOCR)
[![License-MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

本專題開發了一套適用於**戶外動態環境**的智慧校園車牌辨識系統。針對校園門禁常見的車輛歪斜進站、夜間大燈直射反光、雨天水滴干擾等痛點，本系統揚棄了傳統高度依賴邊緣偵測的 OCR 技術，採用三位一體的深度學習架構（CRAFT + CNN + BiLSTM），實現了**低延遲、高強韌性的邊緣運算（Edge Computing）** 門禁控制。

---

## 🚀 系統核心技術架構 (Technical Architecture)

本系統的文字辨識管線（OCR Pipeline）主要由以下三大深度學習模塊組成：

### 1. 文字偵測核心：CRAFT 演算法
* **字元意識區域定位（Character Region Awareness）：** 預測影像中單個字元的中心點位置，生成 **區域得分（Region Score）** 機率熱力圖（越靠近字體中心越紅）。
* **字元親和力連結（Character Affinity Linkage）：** 計算相鄰字元間的空間關聯，生成 **親和力得分（Affinity Score）** 熱力圖，將離散的英數字元黏合成完整的車牌區域。
* **幾何畸變容錯：** 完美克服車輛駛入時的斜切、彎曲與低角度仰拍變形。

<p align="center">
  <img src="image_b0b8df.jpg" width="600" alt="CRAFT Text Detection Heatmap"/>
  <br>
  <em>圖 1. CRAFT 演算法之字元區域意識熱力圖與邊界框生成示意圖 (Baek et al., 2019)</em>
</p>

### 2. 特徵提取核心：CNN (LeNet-5 拓撲架構)
* **動態特徵掃描：** 透過多組卷積核（Filters）與特徵圖（Feature Maps），動態提取車牌英數之邊緣、橫線、直線與幾何弧度特徵。
* **光學環境抗噪（Subsampling/Pooling）：** 進行矩陣降維與壓縮，**自動過濾戶外強烈車燈反光與雨天水滴噪點**。
* **平移不變性（Translation Invariance）：** 車牌不論在畫面中偏左、偏右、或因距離遠近而放大縮小，皆能穩定鎖定結構。

<p align="center">
  <img src="image_b133a7.jpg" width="600" alt="LeNet-5 CNN Architecture"/>
  <br>
  <em>圖 2. 經典 LeNet-5 卷積神經網路拓撲架構圖 (LeCun et al., 1998)</em>
</p>

### 3. 時序識別核心：BiLSTM 雙向循環序列網路
* **雙向上下文記憶：** 整合正向隱藏層（由左至右）與反向隱藏層（由右至左），同時模擬人類順序與逆向回溯的閱讀邏輯，捕捉字元間的前後時序關聯。
* **極致字元容錯：** 當車牌因污漬磨損導致局部模糊（如字母 `B` 與數字 `8` 混淆）時，系統能藉由前後文雙向機率，**自動動態校正並融合字元**。
* **CTC 動態序列解碼：** 完美黏合離散的英數字元，精準解碼為最終的車牌純文字字串（如 `"ABC5678"`）。

<p align="center">
  <img src="image_b14346.png" width="600" alt="BiRNN Architecture"/>
  <br>
  <em>圖 3. BiRNN/BiLSTM 雙向循環序列時間展開架構圖 (Schuster & Paliwal, 1997)</em>
</p>

---

## 💎 專題實務應用優勢 (Key Advantages)

1. **擺脫外網束縛的邊緣運算 (Edge Computing)：** 
   模型經高度優化與輕量化，在 Python 程式中設定 `gpu=False` 依然能於本地端 CPU 進行毫秒級推理，實現低延遲、低成本的智慧門禁控制。
2. **高幾何容錯與光學抗噪：** 
   結合雙通道熱力圖與雙向序列記憶，徹底解決傳統辨識技術在陰影、反光、天候不佳與角度偏差時頻繁誤判的實務痛點。

---

## 🛠️ 開發環境與依賴套件 (Installation & Dependencies)

本專題基於 **Python 3.8+** 環境開發，請確保已安裝以下核心套件：

```bash
# 複製專案庫
git clone [https://github.com/您的帳號/您的專案名稱.git](https://github.com/您的帳號/您的專案名稱.git)
cd 您的專案名稱

# 安裝核心依賴套件
pip install easyocr pandas scipy seaborn pillow
