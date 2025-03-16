import requests
import datetime

# Define HTTP methods to test
METHODS = ["GET", "HEAD", "OPTIONS", "TRACE", "PUT", "DELETE"]

# Define User-Agents to bypass WAF
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0 Safari/537.36",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)"
]

# Read sensitive paths from a text file
def load_paths(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)

# Test access to each path with different methods and User-Agents
def check_paths(base_url, paths):
    log_file = f"scan_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"Security Scan - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write("=" * 80 + "\n")

        for path in paths:
            for method in METHODS:
                for user_agent in USER_AGENTS:
                    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
                    headers = {"User-Agent": user_agent}

                    try:
                        response = requests.request(method, url, headers=headers, timeout=5)
                        status = response.status_code
                        message = response.reason  # Get response message
                        
                        log_entry = f"{datetime.datetime.now().strftime('%H:%M:%S')} | {method} {url} | {status} {message} | {user_agent}\n"
                        print(log_entry.strip())
                        log.write(log_entry)

                    except requests.exceptions.RequestException as e:
                        log.write(f"ERROR: {method} {url} | {str(e)}\n")

        log.write("=" * 80 + "\nScan Completed.\n")

# Main Execution
if __name__ == "__main__":
    base_url = input("Enter the target domain (e.g., https://example.com): ").strip()
    file_path = input("Enter the path to the text file containing sensitive paths: ").strip()

    paths = load_paths(file_path)
    check_paths(base_url, paths)
