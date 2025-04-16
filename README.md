# LoggerBridge

LoggerBridge is a Python-based web application designed to interact with Modbus devices, read their registers, and log the results. It provides a simple and extensible framework for monitoring and managing Modbus devices through a web interface.

This project is developed for **Entec Contractors SA** to facilitate reading registers from various loggers and interacting with them efficiently. It is tailored for industrial automation and IoT applications.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Web Interface](#web-interface)
- [Docker Usage](#docker-usage)

---

## Overview

LoggerBridge is designed to:
- Connect to Modbus devices using their IP address, port, and unit ID.
- Read specific registers from the devices.
- Log the raw values of the registers for monitoring and debugging purposes.
- Provide a web interface to control loggers (start/stop) and view outputs dynamically.

---

## Features

- **Web Interface**: A Flask-based web application to interact with loggers.
- **Logger Reader**: Read and log register values from Modbus devices.
- **Logger Control**: Start or stop loggers via the web interface.
- **Dynamic Output**: View script outputs and logs directly in the browser.
- **Docker Support**: Run the application in a Docker container for easy deployment.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)
- Required Python packages:
  - `pymodbus`
  - `flask`
  - `flask-wtf`
  - `flask-cors`
- Docker (optional, for containerized deployment)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/loggerbridge.git
   cd loggerbridge
   ```

2. Install the required Python packages:
   ```bash
   pip install -r package/requirements.txt
   ```

---

## Usage

### Running the Application Locally
1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Web Interface

### Features
1. **Run Logger Reader**:
   - Reads registers from Modbus devices and displays the output in the browser.
   - Logs are dynamically rendered in the "Output" section.

2. **Control Logger**:
   - Start or stop loggers via the web interface.
   - Displays the success or error messages in the browser.

### Example Workflow
1. Open the web interface at `http://127.0.0.1:5000`.
2. Use the "Run Logger Reader" button to read registers from Modbus devices.
3. Use the "Start Logger" or "Stop Logger" buttons to control the logger.

### Output Example
#### Success:
```
Output:
Starting the logger...
Result: True
Logger started successfully.
```

#### Logs or Errors:

Example from Fronius:
```
Error or Logs:
2025-04-16 11:42:42,734 - INFO - 📖 Read from address 40241: [1]
2025-04-16 11:42:42,735 - INFO - ✅ SUCCESS - Plant Status (Address: 40241): [1]
```

---

## Docker Usage

### Prerequisites
- Docker installed on your system.

### Steps to Run with Docker

1. **Build the Docker Image**:
   Navigate to the `package` folder and build the Docker image:
   ```bash
   docker-compose -f package/docker-compose.yml build
   ```

2. **Run the Docker Container**:
   Start the container using Docker Compose:
   ```bash
   docker-compose -f package/docker-compose.yml up
   ```

3. **Access the Application**:
   Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

4. **Stop the Container**:
   To stop the container, press `Ctrl+C` or run:
   ```bash
   docker-compose -f package/docker-compose.yml down
   ```

---

## Development Notes

### Flask Routes
- `/`: Displays the main web interface.
- `/run`: Handles `POST` requests to execute scripts (`logger_reader.py` or `logger_control.py`).

### Scripts
- **`logger_reader.py`**:
  - Reads registers from Modbus devices and logs the results.
  - Requires a `category` argument to specify the device type.
- **`logger_control.py`**:
  - Controls the logger (start/stop) by writing to specific Modbus registers.
  - Requires `action` (start/stop) and `category` arguments.

---

## Example `devices.csv`

Ensure your `devices.csv` file contains the correct categories and device information:
```csv
category,ip,port,unit_id,register_address,register_name,scale,unit
huawei,10.100.7.163,502,100,40202,Plant Status,1,
sungrow,10.100.2.163,502,247,8001,Plant Status,1,
froniusGen24,10.108.1.51,502,1,40193,PV inverter state,1,
froniusDatamanager,10.100.2.161,502,1,40193,Plant Status,1,
```

---

## Notes
- Ensure that the `category` passed from the web interface matches the `category` values in `devices.csv`.
- Test the application thoroughly to verify that all dependencies and configurations are working correctly in both local and Docker environments.