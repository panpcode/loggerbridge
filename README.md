# LoggerBridge

LoggerBridge is a Python-based application designed to interact with Modbus devices, read their registers and log the results. It provides a simple and extensible framework for monitoring and managing Modbus devices.

This project is developed for **Entec Contractors** to facilitate reading registers from various loggers and interacting with them efficiently. It is tailored for industrial automation and IoT applications.

---

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)

---

## Overview

LoggerBridge is designed to:
- Connect to Modbus devices using their IP address, port, and unit ID.
- Read specific registers from the devices.
- Log the raw values of the registers for monitoring and debugging purposes.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)
- pymodbus
  ``` bash
      panpap@192 loggerbridge % pip show pymodbus                                          
         Name: pymodbus
         Version: 2.5.3
         Summary: A fully featured modbus protocol stack in python
         Home-page: https://github.com/riptideio/pymodbus/
         Author: Galen Collins
         Author-email: bashwork@gmail.com
         License: BSD-3-Clause
         Location: /Users/panpap/Library/Python/3.9/lib/python/site-packages
         Requires: pyserial, six
         Required-by: 

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/loggerbridge.git
   cd loggerbridge
   # read loggers
   python logger_reader.py
   # control loggers
   python logger_control.py