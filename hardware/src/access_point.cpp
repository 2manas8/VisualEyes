#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

extern String ssid;
extern String pass;
extern bool credentialsReceived;

WebServer server(80);

void handleRoot() {
  String page = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>WiFi Setup</title></head><body>";
  page += "<h3>ESP32-CAM WiFi Setup</h3>";
  page += "<form action='/set' method='GET'>";
  page += "SSID: <input name='ssid' length=32><br><br>";
  page += "Password: <input name='pass' length=64 type='password'><br><br>";
  page += "<input type='submit' value='Save & Connect'>";
  page += "</form></body></html>";
  server.send(200, "text/html", page);
}

void handleSet() {
  if (server.hasArg("plain")) {
    String body = server.arg("plain");
    Serial.println("JSON received: " + body);
    
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, body);
    
    if (!error) {
      ssid = doc["ssid"].as<String>();
      pass = doc["pass"].as<String>();
    } else {
      Serial.println("JSON parse error: " + String(error.c_str()));
      server.send(400, "text/plain", "Invalid JSON");
      return;
    }
  } else {
    ssid = server.arg("ssid");
    pass = server.arg("pass");
    Serial.println("GET params - SSID: " + ssid);
  }
  
  if (ssid.length() == 0 || ssid.length() > 32) {
    server.send(400, "text/plain", "ERROR: Invalid SSID");
    Serial.println("Invalid SSID length");
    return;
  }
  
  credentialsReceived = true;
  
  String page = "<!DOCTYPE html><html><body>";
  page += "<h3>Credentials saved!</h3>";
  page += "<p>SSID: " + ssid + "</p>";
  page += "<p>Connecting...</p>";
  page += "</body></html>";
  
  server.send(200, "text/html", page);
  Serial.println("Credentials received: " + ssid);
  
  server.stop();
}

void accessPointSetup() {
  WiFi.mode(WIFI_AP);
  WiFi.softAP("ESP32-CAM-SETUP", "12345678");
  
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  
  server.on("/", handleRoot);
  server.on("/set", handleSet);
  server.begin();
  Serial.println("WiFi Setup server started");
  Serial.println("Connect to 'ESP32-CAM-SETUP' and visit http://" + IP.toString());
}