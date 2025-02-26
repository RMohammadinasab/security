import requests
import time

#Function to read payloads
def load_payloads(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("[!] file payloads.txt is not found!")
        return []

#Test XSS 
def test_xss(url, param, payload_file, method="GET", timeout=5, log_file="xss_log.txt"):
    payloads = load_payloads(payload_file)
    if not payloads:
        print("[!] Payload file is empty!")
        return
    
    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"🔍 testing XSS on {url}  with method {method}\n")
        log.write("=" * 60 + "\n")

        for payload in payloads:
            data = {param: payload}
            try:
                if method.upper() == "GET":
                    response = requests.get(url, params=data, timeout=timeout)
                else:
                    response = requests.post(url, data=data, timeout=timeout)

                #  Display User info 
                output = (
                    f"🔎 testing with : {payload}\n"
                    f"📡 URL: {response.url}\n"
                    f"📥 Response Code: {response.status_code}\n"
                    f"📑 Headers:\n{response.headers}\n"
                    + "=" * 60 + "\n"
                )

                print(output)
                log.write(output)

                # Check XSS vulnerability
                if payload in response.text:
                    print(f"🔥 XSS vulnerability is found! (Payload: {payload})")
                    log.write(f"🔥 XSS vulnerability is found! (Payload: {payload})\n")
                else:
                    print("✅ It seems secure.")
                    log.write("✅ It seems secure.\n")

            except requests.exceptions.RequestException as e:
                print(f"[⚠️] Error in sending the request: {e}")
                log.write(f"[⚠️] Error in sending the request: {e}\n")

# Get user inputs
if __name__ == "__main__":
    url = input("🔹 Please enter the target URL: ").strip()
    param = input("🔹 input parameter (for example: s): ").strip()
    payload_file = input("🔹 Enter your path payloads.txt  : ").strip()
    method = input("🔹 methode (GET/POST): ").strip().upper()
    
    # Execute XSS
    test_xss(url, param, payload_file, method=method)
