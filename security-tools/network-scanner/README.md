# Network Scanner Tool
This tool scans a given IP range or subnet to identify live hosts and open ports. It provides information about running services on detected open ports.

## Features
- Scans a given subnet and detects live hosts.
- Identifies open ports and the running services.
- Supports scanning popular ports (SSH, HTTP, HTTPS, databases, Redis, Grafana, etc.).
- Outputs results in a readable format.


## Installation

Ensure you have Python installed. Then, install the required dependencies using:

```bash
pip install nmap
```




## Usage

1. Create a text file `ips.txt` containing subnets (e.g., `192.168.1.0/24`).
2. Run the script:

```bash
python scan.py
```


## Example Output

```bash
Scanning 192.168.1.1 ...
Scanning 192.168.1.2 ...
Live Hosts:
==================================================
192.168.1.1 is UP:
  Port 22: ssh
  Port 80: http
--------------------------------------------------
192.168.1.5 is UP:
  Port 3306: mysql
--------------------------------------------------
```

## Requirements
- Python 3.x
- Nmap (`sudo apt install nmap` on Linux)
- Internet connection (for external scans)


## License
This project is licensed under the MIT License.


## Contact
For questions or feedback, reach out via:
- Email: rm.nasab@gmail.com
- LinkedIn: [Razieh Mohammadinasab](https://www.linkedin.com/in/razieh-mohammadinasab-32b57238/)
