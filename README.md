# RC Car Controlled by Raspberry Pi

A Raspberry Pi–powered RC car that supports manual keyboard control, PWM-based motor and steering control, and serves as a foundation for autonomous vehicle features.

This project demonstrates embedded systems programming, hardware–software integration, and real-time control using Python.

---

## 🚗 Project Overview

This RC car replaces the traditional remote controller with a Raspberry Pi, allowing the car to be controlled programmatically. The system uses GPIO-based PWM signals to control:

- Electronic Speed Controller (ESC) for throttle
- Servo motor for steering
- Optional camera module for live video streaming

The project is designed with modularity in mind, enabling future expansion into autonomous navigation and obstacle detection.

---

## 🛠️ Hardware Components

- Raspberry Pi (Model ___)
- RC car chassis
- Electronic Speed Controller (ESC)
- DC motor
- Servo motor (steering)
- LiPo battery
- Buck converter (voltage regulation)
- Jumper wires
- Optional: Raspberry Pi Camera Module

---

## 💻 Software & Technologies

- Python
- Raspberry Pi OS
- RPi.GPIO / gpiozero
- PWM (Pulse Width Modulation)
- SSH / VNC (remote control & debugging)

---

## 🎮 Features

- Keyboard-based manual control (W/A/S/D)
- PWM speed control for smooth acceleration
- Servo-based steering control
- Modular code structure
- Remote access via SSH/VNC
- Expandable architecture for autonomous driving

---

DEMO VIDS

https://www.youtube.com/shorts/wvcTN9s7A-8
RC CAR MOVEMENT
https://youtube.com/shorts/ZTLsMX7iXtQ?feature=share






## 📂 Project Structure

```bash
RC-CAR-RASPBERRY-PI/
│
├── motor.py        # ESC motor control logic
├── servo.py        # Steering control
├── control.py      # Keyboard input and main loop
├── camera.py       # (Optional) camera streaming
├── requirements.txt
└── README.md



