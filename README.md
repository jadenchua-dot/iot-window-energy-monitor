# iot-window-energy-monitor
An IoT prototype built with Arduino Uno, Raspberry Pi, Flask, and MariaDB to monitor window status, enforce ventilation grace periods, and prevent air-conditioning energy wastage
# 🪟 Smart Window Energy Guard (IoT Prototype)

An automated IoT-based system designed to prevent electricity wastage in air-conditioned environments by monitoring window status and enforcing a customizable ventilation grace period[cite: 3]. 

Developed by **Jaden Chua** for the Diploma in Electronic and Computer Engineering (C89) at Nanyang Polytechnic[cite: 3].

---

## 📋 Table of Contents
- [Executive Summary](#executive-summary)
- [System Architecture](#system-architecture)
- [Tech Stack & Hardware](#tech-stack--hardware)
- [Key Features](#key-features)
- [File Structure](#file-structure)
- [Testing & Results](#testing--results)

---

## 🚀 Executive Summary

In tropical climates like Singapore, air conditioning accounts for a major portion of building electricity consumption[cite: 3]. A common source of energy wastage occurs when windows are left open while air conditioning is running, allowing cool air to escape[cite: 3]. 

The **Smart Window Energy Guard** solves this by acting as a "smart timer" for your window[cite: 3]. It gives users a customizable **grace period (5–60 seconds)** for necessary ventilation[cite: 3]. If the window remains open past the allowed time limit, a red LED and buzzer are triggered to alert the user[cite: 3].

---

## 🏗️ System Architecture

The system operates on a four-step continuous cycle combining an Arduino microcontroller and a Raspberry Pi gateway[cite: 3]:

1. **Sensing:** The Arduino Uno reads the Infrared Reflective Sensor (window state) and Rotary Angle Sensor (time limit)[cite: 3].
2. **Data Transmission:** Raw sensor signals are streamed to the Raspberry Pi via a USB serial connection[cite: 3].
3. **Processing & Logic:** A Python script on the Raspberry Pi evaluates whether the window has exceeded the user-defined time limit[cite: 3].
4. **Alerts & Storage:** If time is exceeded, a signal is sent back to the Arduino to activate the LED/Buzzer alarm[cite: 3], while event details are logged into a MariaDB database and displayed on a Flask web dashboard[cite: 3].

---

## 🧰 Tech Stack & Hardware

### Hardware Components
* **Arduino Uno:** Controller for sensor reading and alarm activation[cite: 3].
* **Grove Infrared Reflective Sensor:** Detects whether the window is open or closed[cite: 3].
* **Grove Rotary Angle Sensor:** Allows users to manually set the timer grace period (5–60 seconds)[cite: 3].
* **Red LED & Buzzer:** Visual and audio alert mechanisms[cite: 3].
* **Raspberry Pi:** Gateway for central logic processing, database handling, and web hosting[cite: 3].

### Software & Frameworks
* **C++ (Arduino IDE):** Programs the Arduino Uno to handle sensor inputs and output alarms[cite: 3].
* **Python v3 (Thonny IDE):** Handles system logic, timing control, and serial communication (`pySerial`)[cite: 3].
* **MariaDB & PyMySQL:** Relational database system used to store window activity history[cite: 3].
* **Flask Web Framework:** Hosts a real-time web dashboard displaying live system status and logs[cite: 3].

---

## ✨ Key Features

* **Customizable Ventilation Grace Period:** Users can adjust the timer dynamically using a rotary knob[cite: 3].
* **Centralized Logic Control:** Raspberry Pi manages decision-making and sends command triggers back to the Arduino[cite: 3].
* **Automated Data Logging:** Every event is securely saved with timestamps, window states, and alert statuses into MariaDB[cite: 3].
* **Web-Based Dashboard:** A Flask-powered web interface visualizes real-time room security and historical energy-wastage events[cite: 3].

---

## 📂 File Structure

```text
smart-window-energy-guard/
├── arduino/
│   └── window_sensor.ino
