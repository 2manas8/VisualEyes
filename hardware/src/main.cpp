#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

extern String ssid;
extern String pass;
extern bool credentialsReceived;
extern WebServer server;

extern void cameraSetup();
extern void accessPointSetup();
extern void startCameraServer();
extern void setupLedFlash();
extern void sendLocalIPToServer(String);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  accessPointSetup();
  
  unsigned long startTime = millis();
  while (!credentialsReceived && (millis() - startTime < 300000)) {
    server.handleClient();
    delay(100);
  }
  
  if (credentialsReceived) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid.c_str(), pass.c_str());
    WiFi.setSleep(false);
    
    Serial.print("WiFi connecting");
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 30) {
      delay(500);
      Serial.print(".");
      attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("");
      Serial.println("WiFi connected");
      
      cameraSetup();
      startCameraServer();

      sendLocalIPToServer(WiFi.localIP().toString());
    } else {
      Serial.println("WiFi failed - restarting...");
      ESP.restart();
    }
  }
}

void loop() {
  if (credentialsReceived && WiFi.status() == WL_CONNECTED) {
    delay(10000);
  } else {
    server.handleClient();
    delay(100);
  }
}