# 📡 基於 AIoT 架構之不設限場景智慧文字與車牌辨識系統
> **An End-to-End Smart License Plate & Text Recognition System Powered by AIoT Architecture**

本專案實作了一套具備「邊緣端智慧採集、可靠網路傳輸、後端核心深度學習運算與即時自動推播」的完整 **AIoT（人工智慧物聯網）** 系統。系統成功打破傳統物聯網「前端盲目採集、後端網路擁堵」的限制，透過現代深度學習演算法賦予前端硬體智慧大腦，在複雜、變形、角度傾斜的不設限場景（Unconstrained Scenarios）中，仍能交出極高魯棒性（Robustness）的文字辨識答卷。

---

## 🚀 核心功能 (System Features)

* **📷 邊緣端智慧採集控制：** 使用低成本、高效能的硬體單元，控制鏡頭進行物理訊號擷取，並進行影像智能快取。
* **📐 克服多角度傾斜與變形：** 拋棄傳統死板的「字元切割」技術，能精準辨識路邊斜拍、凹損或反光的車牌與變體字型。
* **🧠 端到端深度學習解碼：** 核心整合像素級文字偵測、高階視覺特徵提取與前後文時序序列關係捕捉，實現 Segmentation-free 的高效能辨識。
* **📲 自動化智慧通知閉環：** 後端平台自動化分析影像，辨識成功後無需人工介入，即時透過通訊平台進行結果推播。

---

## 🏗️ AIoT 系統垂直架構 (Vertical Architecture)

本系統完全採用現代 **AIoT 垂直分層模型** 進行架構設計，落實了從前端感知到後端決策的完整資料流閉環：
1. **感測層 (Sensing Layer)：** 透過 `OV2460` 鏡頭擷取光學訊號，由 `ESP32-CAM` 作為邊緣控制單元，扮演專為 AI 模型優化的智慧感知單元。
2. **網路層 (Networking Layer)：** 透過本地 `Wi-Fi` 無線區域網路與 `HTTP` 傳輸協定，將原始影像數據高效、即時地推送至中央平台。
3. **平台層 (Platform Layer)：** 系統的智慧核心，基於 `Python / Streamlit` 可視化平台，垂直整合現代深度學習演算法進行核心運算。
4. **應用層 (Application Layer)：** 最終辨識成果自動對接 `LINE Notify` API，落實即時警報與端點通知的智慧應用。

---

## 🧩 AIoT 三環核心實踐 (Core Technology Subsystems)

呼應國際物聯網權威文獻框架，本專案將技術具體深化為三大核心環節的交織實踐：

### 1. Sensing (AI 賦能邊緣感知)
* **硬體佈署：** ESP32-CAM 邊緣控制單元 + OV2460 光學鏡頭組。
* **設計理念：** 前端設備專為深度學習模型之輸入需求進行優化，進行智慧採集，非傳統被動式盲目錄影。

### 2. Networking (可靠數據傳輸)
* **通訊協定：** Wi-Fi 無線網路技術 + HTTP 高速傳輸協議。
* **傳輸特性：** 確保前端採集到的高質量影像流能夠跨層級、低延遲地傳遞，提供系統即時分析的基石。

### 3. Computing (現代 AI 運算大腦) 🌟 *Core Breakthrough*
本專案整合後端 `EasyOCR` 開源框架，在運算核心注入三大頂級 AI 演算法，徹底克服傳統影像處理（如 Sobel 邊緣檢測、垂直投影切割）害怕反光與歪斜的致命傷：
* **CRAFT 演算法 (Character Region Awareness)：** 拋棄傳統硬切割，改用像素級的「區域得分 (Region Score)」與「親和力得分 (Affinity Score)」預測文字中心與關聯性，具備極強的角度抗干擾能力。
* **現代 CNN (卷積神經網路)：** 自動提取高階視覺特徵，取代傳統手工設計規則。
* **LSTM + CTC (長短期記憶網路與連接時序分類)：** 捕捉前後文時序序列關係，進行免切割的端到端（End-to-End）序列解碼。

---

## 📚 參考文獻與學術支持 (References)

本專案之架構設計與演算法選型皆具備嚴謹的學術理論支撐：

* **[1] AIoT 架構總覽：**
    Siam, A. I., et al. (2024). Artificial Intelligence of Things: A Survey. *ACM Transactions on Sensor Networks (TOSN)*.
* **[2] 文字偵測演算法 (CRAFT 官方論文)：**
    Baek, Y., Lee, B., Han, D., Yun, S., & Lee, H. (2019). Character region awareness for text detection. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. 9365-9374).
* **[3] 卷積神經網路 (CNN 經典論文)：**
    Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. *Advances in Neural Information Processing Systems (NeurIPS)*, 25, 1097-1105.
* **[4] 長短期記憶網路 (LSTM 創始論文)：**
    Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(1), 1-45.
* **[5] 整合開發框架 (EasyOCR 開源出處)：**
    JaidedAI. (2020). *EasyOCR: Ready-to-use OCR with 80+ supported languages and all popular writing scripts*. GitHub Repository. https://github.com/JaidedAI/EasyOCR
