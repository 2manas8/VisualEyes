#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include "ultrasonic.h"

extern String ssid;
extern String pass;
extern bool credentialsReceived;
extern WebServer server;

extern void cameraSetup();
extern void accessPointSetup();
extern void startCameraServer();
extern void setupLedFlash();
extern void sendLocalIPToServer(String);
extern void enableNavigation();
extern void disableNavigation();

namespace {
constexpr uint8_t ultrasonicTriggerPin = 14;
constexpr uint8_t ultrasonicEchoPin = 2;
constexpr float obstacleDistanceCm = 100.0f;
constexpr unsigned long ultrasonicPollIntervalMs = 1000;

bool navigationEnabled = false;
bool obstacleDetected = false;
unsigned long lastUltrasonicPollMs = 0;

void setNavigationEnabled(bool enabled) {
  if (navigationEnabled == enabled) {
    return;
  }

  if (enabled) {
    enableNavigation();
  } else {
    disableNavigation();
  }

  navigationEnabled = enabled;
}

void handleObstacleNavigation() {
  unsigned long now = millis();
  if (now - lastUltrasonicPollMs < ultrasonicPollIntervalMs) {
    return;
  }
  lastUltrasonicPollMs = now;

  bool objectAhead = isObjectWithinDistanceCm(obstacleDistanceCm);
  if (objectAhead == obstacleDetected) {
    return;
  }

  obstacleDetected = objectAhead;
  setNavigationEnabled(!obstacleDetected);
}
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  setupUltrasonicSensor(ultrasonicTriggerPin, ultrasonicEchoPin);
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
      setNavigationEnabled(true);
    } else {
      Serial.println("WiFi failed - restarting...");
      ESP.restart();
    }
  }
}

void loop() {
  if (credentialsReceived && WiFi.status() == WL_CONNECTED) {
    handleObstacleNavigation();
    delay(10);
  } else {
    server.handleClient();
    delay(100);
  }
}
