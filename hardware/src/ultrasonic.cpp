#include "ultrasonic.h"

namespace {
uint8_t triggerPin = 0;
uint8_t echoPin = 0;

constexpr unsigned long triggerPulseUs = 10;
constexpr unsigned long maxEchoTimeUs = 12000;
constexpr float speedOfSoundCmPerUs = 0.0343f;
}

void setupUltrasonicSensor(uint8_t triggerPinNumber, uint8_t echoPinNumber) {
  triggerPin = triggerPinNumber;
  echoPin = echoPinNumber;

  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(triggerPin, LOW);
}

float readUltrasonicDistanceCm() {
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(triggerPulseUs);
  digitalWrite(triggerPin, LOW);

  unsigned long durationUs = pulseIn(echoPin, HIGH, maxEchoTimeUs);
  if (durationUs == 0) {
    return -1.0f;
  }

  return (durationUs * speedOfSoundCmPerUs) / 2.0f;
}

bool isObjectWithinDistanceCm(float distanceCm) {
  float measuredDistanceCm = readUltrasonicDistanceCm();

  return measuredDistanceCm > 0.0f && measuredDistanceCm <= distanceCm;
}
