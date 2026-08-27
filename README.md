# CardioSense ECG

**An AI-powered ECG monitoring prototype for real-time heart abnormality detection using TinyML.**

CardioSense combines an AD8232 ECG sensor, an ESP32 microcontroller, and a one-dimensional Convolutional Neural Network (1D CNN) to capture ECG signals and classify heartbeats as normal or abnormal.

> **Project status:** In development. Live ECG acquisition and visualization are working. Real-time TinyML classification on the ESP32 is the current phase.

## Project Overview

Cardiovascular abnormalities may not always be identified early, particularly where continuous monitoring equipment is unavailable or expensive. CardioSense explores a portable, low-cost approach to ECG monitoring and on-device abnormality detection.

The system is designed to:

- Capture ECG signals using the AD8232 sensor
- Sample ECG data through the ESP32
- Process 200-sample heartbeat windows
- Run a TensorFlow Lite model on the ESP32
- Classify heartbeats as normal or abnormal
- Transmit results for external visualization

## System Architecture

```text
ECG Electrodes
      ↓
AD8232 ECG Sensor
      ↓
ESP32 Microcontroller
      ↓
Signal Processing
      ↓
TinyML CNN Inference
      ↓
Normal / Abnormal Classification
      ↓
Bluetooth or Serial Output
