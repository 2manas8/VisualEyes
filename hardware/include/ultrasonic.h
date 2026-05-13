#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include <Arduino.h>

void setupUltrasonicSensor(uint8_t triggerPin, uint8_t echoPin);
float readUltrasonicDistanceCm();
bool isObjectWithinDistanceCm(float distanceCm);

#endif
