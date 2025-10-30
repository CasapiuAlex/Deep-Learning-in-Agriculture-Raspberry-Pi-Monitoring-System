# Deep Learning in Agriculture: Raspberry Pi Monitoring System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This repository contains the bachelor's thesis project "Deep Learning in Agriculture: Raspberry Pi System for Pest Detection and Plant Disease Classification." The project consists of an autonomous, integrated system that uses two artificial intelligence models for real-time monitoring of crop health.

![Web Interface Demo](images/web_ui.gif)
<img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/3d8e8651-5b07-4958-a75c-464f3d31b467" />

## Table of Contents

- [Project Description](#project-description)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
  - [Hardware](#hardware)
  - [Software](#software)
- [Technologies Used](#technologies-used)
- [Performance & Results](#performance--results)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [License](#license)

## Project Description

The goal of this project is to provide an accessible and effective solution for precision agriculture. The system combines a Raspberry Pi-based hardware platform with two specialized Deep Learning models to automate the plant monitoring process. It can identify pests in real-time and provide a diagnosis of leaf health, helping farmers to intervene quickly and accurately, thereby reducing losses and environmental impact.

## Key Features

-   **Real-Time Pest Detection:** Utilizes an optimized YOLOv12n model to identify and locate 8 classes of pests directly in the video stream.
-   **On-Demand Disease Classification:** Employs a Convolutional Neural Network (CNN) to classify the health status of a leaf (Healthy, Powdery, Rust) from a snapshot.
-   **Intuitive Web Interface:** A centralized web interface, built with Flask, allows for complete control over the system.
-   **Precise Camera Control:** A Pan-Tilt mechanism (2-axis) is controlled via hardware-generated PWM for smooth, jitter-free movement.
-   **Live Video Streaming:** Streams video from the Raspberry Pi camera in MJPEG format with low latency.
-   **Autonomous System:** All processing is performed directly on the Raspberry Pi 5 board.

## System Architecture

### Hardware

The physical assembly is designed for autonomous operation and precise control.

-   **Central Unit:** Raspberry Pi 5
-   **Vision System:** Raspberry Pi Camera Module V2
-   **Movement Mechanism:** 3D-printed Pan-Tilt mount with two servo motors (SG90).
-   **Control & Power:** A custom PCB manages the servo motors, which are powered by a dedicated external power supply to ensure system stability.

<img width="400" height="200" alt="image" src="https://github.com/user-attachments/assets/a9e2cb91-8755-491f-b69d-17e553159b79" />

### Software

The software architecture is modular to ensure efficient and concurrent operation. It consists of a Flask web server that orchestrates the different modules for detection, classification, and hardware control.

1.  **CNN Architecture for Classification:** A custom sequential model built to extract hierarchical features from leaf images.
2.  **YOLO Architecture for Detection:** A modern architecture from yolo12n ideal for real-time object detection tasks.

## Technologies Used

-   **Backend:** Python, Flask
-   **Frontend:** HTML, CSS, JavaScript (Fetch API)
-   **Deep Learning:**
    -   TensorFlow / Keras (for the CNN model)
    -   YOLOv12n (inference with NCNN)
    -   OpenCV
-   **Hardware Control:**
    -   Raspberry Pi OS
    -   GPIO programming for hardware PWM
-   **Development Platforms:**
    -   Google Colab (for model training)
    -   Roboflow (for labeling and augmenting the detection dataset)

## Performance & Results

The trained models demonstrated solid performance in testing:

-   **Classification Model (CNN):**
    -   **Accuracy:** 96.4%
    -   **F1-Score (Macro Avg):** 0.96
-   **Detection Model (YOLOv12n):**
    -   **mAP@0.5:** 89.6%
    -   **Inference Speed on Raspberry Pi 5:** Approx. 10-12 FPS

**Confusion Matrices:**

<img width="384" height="257" alt="image" src="https://github.com/user-attachments/assets/7dbd41a7-75ca-4cfa-b596-e3f168c7c814" /> <img width="384" height="257" alt="image" src="https://github.com/user-attachments/assets/d11595e7-8a0b-4f59-b2ae-9c3cd2410e1d" />


**Precision-Recall Curves:**

<img width="384" height="257" alt="image" src="https://github.com/user-attachments/assets/fa61938a-91d7-4e0a-b011-88a0226d55d6" /> <img width="384" height="257" alt="image" src="https://github.com/user-attachments/assets/fcd49b89-5918-4b0c-8415-f1d7bce74260" />


## Installation & Setup

To run this project, follow the steps below:

1.  **Clone the repository:**
    ```bash
    All the files required to run the application are located in the RaspberryPi_files folder. The other directories contain the model training code and video examples.
    ```

2.  **Create a virtual environment and activate it:**
    ```bash example
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Hardware Setup:**
    -   Connect the Pi Camera to the CSI port.
    -   Connect the servo motors to the GPIO pins specified in the control script and to the external power supply.

5.  **Run the application:**
    ```bash
    python main_site.py
    ```

## Usage

1.  Once the application is running, access the Raspberry Pi's IP address in your browser (e.g., `http://192.168.1.10:5000`).
2.  Use the interface buttons to start/stop the video stream and the detection mode.
3.  Manually control the camera using the "Pan/Tilt Servo Control" section.
4.  Press the "Take Snapshot and Classify" button to get a diagnosis for a leaf.

## Photo examples of detection and classification

<img width="384" height="257" alt="image" src="https://github.com/user-attachments/assets/1da18a81-883e-4b54-9e82-fb7830e9093c" /> <img width="384" height="257" alt="image" src="https://github.com/user-attachments/assets/df82fbe9-8114-493f-ae55-9d16d3b501ca" />



## License

This project is distributed under the MIT License. See the `LICENSE` file for more details.
