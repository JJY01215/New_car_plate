import datetime
import time
import warnings
import cv2
import easyocr
import numpy as np
import requests
import streamlit as st

# 屏蔽 Streamlit 的官方警告
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")
warnings.filterwarnings("ignore", message=".*use_container_width.*")

# =================== 網頁基礎配置 ===================
st.set_page_config(page_title="智能車牌辨識與閘門門禁系統", layout="wide")

st.title("🚧 智能車牌辨識與閘門門禁系統後台")
st.write("前端控制台與即時監控面板")
st.markdown("---")

# =================== 📌 基礎參數設定 ===================
ESP32_IP = "172.20.10.3"
CAPTURE_URL = f"http://{ESP32_IP}/capture"
OPEN_DOOR_URL = f"http://{ESP32_IP}/open"
ALLOWED_PLATES = ["ABC1234", "ABC5678", "ABC-5678", "7777"]

# 💡 填入你剛才在 LINE Developers 拿到的那串超長 Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = "uFHbI+8o1U8yez1l+XeX49ApmXY59K7WKkqVFbxpBvsZwLBXaHKxs1ai/R4S5a4yAWED+m+lsSNvEkVks8Io7Y1c3XDEXLH4YpsrVJcNkjKfxmaTAmdjMYTLFIU6CBS9fGBl693+DiVH4/pamNdxOwdB04t89/1O/w1cDnyilFU="

# 💡 填入你自己的 User ID (在 Messaging API 頁面最下方，一串 U 開頭的字串)
LINE_USER_ID = "U932c52b32c3de90e108da3e55af77548"


# =================== 💡 LINE Messaging API 官方帳號發送函式 ===================
def send_line_message(text_message):
    line_url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": text_message}],
    }
    try:
        # 設定短 timeout，確保完全不卡網頁主畫面影像
        requests.post(line_url, headers=headers, json=payload, timeout=2.0)
    except Exception as e:
        pass


# 初始化 EasyOCR 模型
@st.cache_resource
def load_ocr():
    return easyocr.Reader(["en"], gpu=False)


reader = load_ocr()

# =================== 正統網頁狀態持久化 ===================
if "LOGS" not in st.session_state:
    st.session_state.LOGS = ["⚡ 系統初始化成功，監聽影像中..."]
if "DOOR_OPEN_UNTIL" not in st.session_state:
    st.session_state.DOOR_OPEN_UNTIL = 0.0


# 甩包式開門與官方帳號通知核心
def trigger_gate_open(reason_text, line_msg):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.LOGS.insert(0, f"[{now_str}] 🔓 [動作] {reason_text}")

    # 計時器：5秒內維持開啟狀態
    st.session_state.DOOR_OPEN_UNTIL = time.time() + 5.0

    # 1. 甩包發送開門訊號給 ESP32-CAM
    try:
        cam_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        requests.get(OPEN_DOOR_URL, headers=cam_headers, timeout=0.2)
    except requests.exceptions.Timeout:
        pass
    except Exception as e:
        st.session_state.LOGS.insert(0, f"[{now_str}] ❌ [通訊連線失敗]: {e}")

    # 2. 💡 修正點：調用最新版的官方帳號傳送函式
    send_line_message(line_msg)


# =================== 判斷目前閘門狀態 ===================
current_time = time.time()
if current_time < st.session_state.DOOR_OPEN_UNTIL:
    is_door_opening = True
else:
    if st.session_state.DOOR_OPEN_UNTIL != 0.0:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.LOGS.insert(
            0, f"[{now_str}] 🔒 [安全歸位] 閘門保持時間結束，恢復關閉。"
        )
        st.session_state.DOOR_OPEN_UNTIL = 0.0
    is_door_opening = False

# =================== 網頁版面配置 (左右雙欄) ===================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 停車場即時監控畫面")
    image_holder = st.empty()

with col2:
    st.subheader("🎛️ 控制面板")

    if is_door_opening:
        st.success("🔓 狀態：閘門已開啟 (通行中...)")
    else:
        st.error("🔒 狀態：閘門已關閉 (嚴密監控中)")

    st.markdown("---")
    # 手動開門按鈕
    if st.button("🚨 手動強制開啟閘門", width="stretch"):
        if not is_door_opening:
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            trigger_gate_open(
                reason_text="警衛點擊網頁按鈕放行。",
                line_msg=f"🚨 [手動觸發通知]\n時間: {now_str}\n說明: 系統管理員手動開啟閘門放行。",
            )
            st.rerun()
        else:
            st.warning("閘門正在運作中，請勿重複發送！")

    st.markdown("---")
    st.write(f"📋 **授權通行白名單：** `{ALLOWED_PLATES}`")

    st.markdown("---")
    st.subheader("📜 歷史辨識與通聯紀錄")

    log_text = "\n".join(st.session_state.LOGS[:12])
    st.text_area(
        "系統日誌 (最新在最上)",
        value=log_text,
        height=200,
        disabled=True,
        key=f"log_view_{len(st.session_state.LOGS)}",
    )

# =================== 影像串流與 AI 辨識核心 ===================
# =================== 影像串流與 AI 辨識核心 ===================
try:
    img_resp = requests.get(CAPTURE_URL, timeout=1.5)
    if img_resp.status_code == 200:
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        if frame is not None:
            display_frame = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)

            image_holder.image(rgb_frame, channels="RGB", width="stretch")

            # 車牌辨識
            if not is_door_opening:
                results = reader.readtext(
                    display_frame, decoder="greedy", batch_size=1
                )

                for bbox, text, confidence in results:
                    clean_text = (
                        text.upper().replace(" ", "").replace("-", "").strip()
                    )

                    # 💡 修正點 1：文字長度太短（例如小於 4 個字）直接忽略，防止 "5678" 或 "77" 這種殘缺辨識提早觸發
                    if len(clean_text) < 4:
                        continue

                    if confidence > 0.40:
                        now_str = datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        st.session_state.LOGS.insert(
                            0,
                            f"[{now_str}] 👀 [偵測] 文字: '{clean_text}' (信心度: {confidence:.2f})",
                        )

                        # 白名單比對
                        matched = False
                        for plate in ALLOWED_PLATES:
                            clean_plate = (
                                plate.upper()
                                .replace(" ", "")
                                .replace("-", "")
                                .strip()
                            )

                            # 💡 修正點 2：改用更嚴格的比對。
                            # 只有在完全相同，或者辨識到很長的完整字串包含白名單時才放行
                            if clean_text == clean_plate or (
                                len(clean_text) >= 6 and clean_text in clean_plate
                            ):
                                matched = True
                                break

                        if matched:
                            trigger_gate_open(
                                reason_text=f"車牌 '{clean_text}' 符合白名單，自動放行！",
                                line_msg=f"🎉 [車牌辨識放行]\n時間: {now_str}\n偵測車牌: {clean_text}\n結果: 符合白名單，安全閘門已自動開啟！",
                            )
                            st.rerun()
                            break

except Exception as e:
    pass

time.sleep(0.03)
st.rerun()
