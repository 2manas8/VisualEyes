#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

void sendLocalIPToServer(String localIP) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin("https://visualeyes.onrender.com/api/stream/save_ip");
    http.addHeader("Content-Type", "application/json");
    
    String jsonPayload = "{\"roomId\":\"1\", \"ip\":\"" + localIP + "\"}";
    
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode == 200) {
      String response = http.getString();
      Serial.println("Server response: " + response);
    } else {
      Serial.println("Server POST failed: " + String(httpResponseCode));
    }
    
    http.end();
  }
}