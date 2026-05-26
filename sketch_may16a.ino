#include "esp_camera.h"
#include <WiFi.h>

// =================== 1. 請填入你的 WiFi 資訊 ===================
const char* ssid = "蔣嘉祐的iPhone";
const char* password = "01215JJY";

// =================== 2. 定義 AI-Thinker 腳位 ===================
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

const int servoPin = 13; // 鎖定你目前直連的 GPIO 13

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  Serial.println();

  // 將直連的 GPIO 13 設定為純數位輸出
  pinMode(servoPin, OUTPUT);
  digitalWrite(servoPin, LOW); 

  // 相機基礎設定
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  config.frame_size = FRAMESIZE_SVGA; 
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("相機初始化失敗: 0x%x\n", err);
    return;
  }

  WiFi.begin(ssid, password);
  Serial.print("正在連線至 WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi 連線成功！");

  server.begin();
  Serial.print("控制網址: http://");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available(); 
  if (!client) return;

  String request = client.readStringUntil('\r');
  client.flush();

  // 當收到 Python 的開門指令
  // 當收到 Python 的開門指令
  if (request.indexOf("GET /open") >= 0) {
    // 先立刻回覆 Python，避免 Python 端的 HTTP request 超時卡死
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/plain; charset=utf-8");
    client.println("Connection: close");
    client.println();
    client.println("Gate Opened!");
    client.flush();
    delay(10);
    client.stop(); // 主動斷開，放 Python 回去自由運作

    Serial.println("🔓 收到指令！執行閘門開啟動作...");
    
    // 【修改點】持續發送 90 度脈衝（1.5ms HIGH），送 150 次相當於維持約 3 秒 (150 * 20ms = 3000ms)
    // 這樣馬達在這 3 秒內才會有力量頂住柵欄，不會垂下來
    for (int i = 0; i < 150; i++) {
      digitalWrite(servoPin, HIGH);
      delayMicroseconds(1500); 
      digitalWrite(servoPin, LOW);
      delayMicroseconds(18500);
    }
    
    Serial.println("🔒 保持時間結束，閘門正在恢復原位 (0 度)...");
    // 模擬 0 度脈衝 (0.5ms HIGH, 19.5ms LOW)，送 50 次（約 1 秒）確保完全歸位
    for (int i = 0; i < 50; i++) {
      digitalWrite(servoPin, HIGH);
      delayMicroseconds(500); 
      digitalWrite(servoPin, LOW);
      delayMicroseconds(19500);
    }
    Serial.println("🟢 閘門已關閉，恢復監測。");
  }
  
  // 請求即時影像
  else if (request.indexOf("GET /capture") >= 0 || request.indexOf("GET /") >= 0) {
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
      client.println("HTTP/1.1 500 Internal Server Error");
      return;
    }
    
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: image/jpeg");
    client.print("Content-Length: ");
    client.println(fb->len);
    client.println("Connection: close");
    client.println();
    
    client.write(fb->buf, fb->len);
    esp_camera_fb_return(fb); 
  }
}