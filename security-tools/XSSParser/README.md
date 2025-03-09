# XSSParser - Automated XSS Scanner
📌 Introduction
XSSParser is a penetration testing tool designed to detect Cross-Site Scripting (XSS) vulnerabilities in websites. It automatically tests a list of payloads on a given parameter and analyzes the server's response.

⚙️ Features

✅ Supports GET and POST methods

✅ Reads payloads from a text file

✅ Timeout feature to prevent request hangs

✅ Saves results in a log file (xss_log.txt)

✅ Displays Response Code and Headers

✅ Detects Reflected XSS by analyzing server responses



🚀 Installation & Usage
1️⃣ Install Dependencies
Before running the tool, install the required Python library:

```bash
pip install requests
```


2️⃣ Run the Tool
Execute the script using Python:
```bash
python3 XSSParser.py
```

3️⃣ Required Inputs
The tool will prompt for the following inputs:
🔹 Target URL → The website URL to test
🔹 Parameter → The input parameter to test (e.g., q, search)
🔹 Payload File → Path to a text file containing XSS payloads
🔹 Request Method → Choose GET or POST


🎯 Example Usage
Suppose you want to test example.com, you have a file payloads.txt, and you choose the GET method:

```bash
python3 XSSParser.py
```

Then enter the following inputs:

🔹 Please enter the target URL: https://example.com/search
🔹 Input parameter (for example: s): q
🔹 Enter your payloads file path: payloads.txt
🔹 Method (GET/POST): GET


Example output from the tool:
```bash
🔎 testing with : <script>alert('XSS')</script>
📡 URL: https://example.com/search?q=<script>alert('XSS')</script>
📥 Response Code: 200
📑 Headers:
{'Content-Type': 'text/html; charset=UTF-8', 'Server': 'nginx'}
============================================================
🔥 XSS vulnerability is found! (Payload: <script>alert('XSS')</script>)
```


🛠 Developer

👤 Razieh Mohammadinasab



⚠️ Legal Disclaimer
❌ This tool is intended for educational and authorized penetration testing only.
❌ The user is responsible for any misuse of this tool!


