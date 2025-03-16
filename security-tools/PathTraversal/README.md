# Path Traversal Scanner

## About
This Python script is designed to test for **Path Traversal vulnerabilities** on web applications by sending various payloads and analyzing responses. It automatically detects the target server OS (Windows/Linux) and uses the appropriate payloads.

## Features
- Detects if the target server is Windows or Linux
- Loads the correct payload list based on OS detection
- Supports both **GET and POST** methods
- Logs results in a file for further analysis
- Shows response **status code, headers, and response preview**

## Installation
Ensure you have Python installed. Then, install the required dependencies:

```bash
pip install requests
```

## Usage
Run the script and follow the instructions:

```bash
python path_traversal-scanner.py
```

When prompted, enter the target URL, HTTP method, and parameter name.

## Payloads
- `linux_payloads.txt` → Path Traversal payloads for Linux (Apache, Nginx, etc.)
- `windows_payloads.txt` → Path Traversal payloads for Windows (IIS, ASP.NET, etc.)

## Examples
```bash
Please enter the target URL: https://example.com/download.php
[*] Detecting server operating system...
[+] Server detected as Linux-based.
Enter the Linux payload file (default: linux_payloads.txt): linux_payloads.txt
HTTP method (GET/POST): GET
Enter parameter name: file

[>>] Sending GET request with payload: ../../../../etc/passwd
[+] Response Status Code: 200
```

## Developer
Razieh Mohammadinasab

## Legal Disclaimer
This tool is intended for educational and authorized penetration testing only. The user is responsible for any misuse of this tool.

