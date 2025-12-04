#include <Arduino.h>
#include "esp_camera.h"
#include <WiFi.h>
#include "board_config.h"
// #include <SocketIOclient.h>

const char* ssid = "Airtel_Manas";
const char* password = "youalreadyhavethepassword";

// const char* host = "visualeyes.onrender.com";
// const int port = 443;
// const char* roomId = "1";

// SocketIOclient socket;

void startCameraServer();
void setupLedFlash();

// void socketEvent(socketIOmessageType_t type, uint8_t * payload, size_t length) {
//     switch(type) {
//     case sIOtype_DISCONNECT:
//       Serial.printf("[IOc] Disconnected!\n");
//       break;
//     case sIOtype_CONNECT:
//       Serial.printf("[IOc] Connected to server: %s\n", payload);
//       {
//         String joinMessage = "[\"joinRoom\",\"" + String(roomId) + "\"]";
//         socket.sendEVENT(joinMessage);
//         Serial.println(joinMessage);
//       }
//       {
//         String ip = WiFi.localIP().toString();
//         String jsonPayload = "{\"roomId\":\"" + String(roomId) + "\",\"ip\":\"" + ip + "\"}";
//         String fullMessage = "[\"sendIp\"," + jsonPayload + "]";
//         socket.sendEVENT(fullMessage);
//         Serial.println(fullMessage);
//       }
//       break;
//     }
// }

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

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
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG;  // for streaming
  // config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if (config.pixel_format == PIXFORMAT_JPEG) {
    if (psramFound()) {
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      // Limit the frame size when PSRAM is not available
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    // Best option for face detection/recognition
    config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
    config.fb_count = 2;
#endif
  }

#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t *s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1);        // flip it back
    s->set_brightness(s, 1);   // up the brightness just a bit
    s->set_saturation(s, -2);  // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if (config.pixel_format == PIXFORMAT_JPEG) {
    s->set_framesize(s, FRAMESIZE_HD);
  }

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

#if defined(CAMERA_MODEL_ESP32S3_EYE)
  s->set_vflip(s, 1);
#endif

// Setup LED FLash if LED pin is defined in camera_pins.h
#if defined(LED_GPIO_NUM)
  setupLedFlash();
#endif

  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  Serial.print("WiFi connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();

  // socket.beginSSL(host, port, "/socket.io/?EIO=4", "wss");
  // socket.onEvent(socketEvent);

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void loop() {
  // Do nothing. Everything is done in another task by the web server
  // socket.loop();
  delay(10000);
}

// #include <Arduino.h>
// #include <WiFi.h>
// #include <WiFiClientSecure.h>

// const char* ssid = "Airtel_Manas";
// const char* password = "youalreadyhavethepassword";
// const char* host = "visualeyes.onrender.com";

// void setup() {
//   Serial.begin(115200);
//   Serial.println();

//   WiFi.begin(ssid, password);
//   Serial.print("Connecting to WiFi");
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }
//   Serial.println("\nConnected!");

//   // --- DIAGNOSTIC TEST ---
//   WiFiClientSecure client;
//   client.setInsecure(); // Ignore certificates
  
//   Serial.print("Connecting to Render...");
//   if (client.connect(host, 443)) {
//     Serial.println("\nSUCCESS! Connected to Render.");
    
//     // Send a raw HTTP request to prove we can talk
//     client.println("GET / HTTP/1.1");
//     client.println("Host: visualeyes.onrender.com");
//     client.println("Connection: close");
//     client.println();
    
//     while (client.connected()) {
//       String line = client.readStringUntil('\n');
//       if (line == "\r") break;
//       Serial.println(line); // Print response headers
//     }
//   } else {
//     Serial.println("\nFAILED! Could not connect to Render.");
//     Serial.print("Error code: ");
//     Serial.println(client.lastError(NULL,0));
//   }
// }

// void loop() {}