# Network Activity Monitor

## Overview
This Python script monitors all network activity on your computer and reports the amount of data sent and received by each network interface over a 30-second interval. It's a handy tool for network diagnostics and monitoring.

## Features
- Monitors network activity in real-time.
- Reports data sent and received by each network interface.
- Simple and easy to use.

## Requirements
- Python 3.x
- `psutil` library

## Installation
1. Ensure that Python 3.x is installed on your system.
2. Install `psutil` if it's not already installed:
   ```bash
   pip install psutil
Usage
Run the script with Python. No additional arguments are required:


python network_activity_monitor.py
How it Works
The script uses the psutil library to access system network details. It retrieves the initial network statistics, waits for 30 seconds, and then retrieves the final network statistics. The difference between these statistics represents the network activity during this interval.

Contributing
Contributions to this project are welcome! Please fork the repository and submit a pull request with your improvements.

License
This project is open-source and available under the MIT License.

Disclaimer
This tool is for informational and diagnostic purposes only. Be aware that monitoring network traffic may require administrative privileges on some systems.
