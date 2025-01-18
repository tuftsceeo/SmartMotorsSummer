# Smart Motor with Smart App

A low-cost educational toolkit that combines the Smart Motor (ESP32-based motor controller) with the Smart App web interface to teach machine learning concepts through hands-on robotics projects.

For more information, visit our project website: https://smartmotors.notion.site/

## Key Components

- Smart Motor (ESP32 microcontroller running MicroPython)
- Smart App (browser-based training interface)
- Integrated motor control and sensor readings
- WebUSB communication between Smart Motor and Smart App

## Project Files

Smart Motor firmware:
- `main.py` - Core Smart Motor functionality including motor control, sensor reading, and serial communication
- `boot.py` - Smart Motor boot configuration
- `servo.py` - Servo motor control library
- `smarttools.py` - Display and UI utilities for the OLED screen
- `ssd1306.py` - OLED display library

[Smart App interface:](https://smart-motors.web.app/) 
- `index.html` - Smart App web interface for motor training and visualization
- `trainData.txt` - Storage for motor training data points

Deployment:
- `firebase.json` - Firebase hosting configuration

## Acknowledgements

This material is based upon work supported by the National Science Foundation under Grant Number IIS-2119174. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.