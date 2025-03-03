import nmap
import ipaddress
import datetime

# Generate all IPs from a given subnet
def generate_ips(subnet):
    """ Generate all IP addresses in a given subnet """
    try:
        network = ipaddress.ip_network(subnet, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        print(f"Invalid subnet: {subnet}")
        return []

# Perform advanced scanning on live hosts
def scan_network(ip_list):
    """ Perform an advanced scan on a list of IPs """
    scanner = nmap.PortScanner()
    live_hosts = {}

    # Logging
    log_file = "scan_results.log"
    with open(log_file, "a") as log:
        log.write("\n" + "=" * 60 + "\n")
        log.write(f"Scan started at {datetime.datetime.now()}\n")
        log.write("=" * 60 + "\n")

        for ip in ip_list:
            print(f"Scanning {ip} ...")

            # Advanced Nmap scan command
            scan_args = "-Pn -p0- -A -T4 --randomize-hosts --data-length 50 --spoof-mac 0"
            scanner.scan(ip, arguments=scan_args)

            if ip in scanner.all_hosts():
                open_ports = []
                log.write(f"\nHost: {ip} (UP)\n")
                log.write("-" * 60 + "\n")

                for proto in scanner[ip].all_protocols():
                    for port in scanner[ip][proto]:
                        state = scanner[ip][proto][port]['state']
                        service = scanner[ip][proto][port].get('name', 'unknown')
                        version = scanner[ip][proto][port].get('version', 'unknown')

                        if state == 'open':
                            port_info = f"Port {port}: {service} (Version: {version})"
                            open_ports.append(port_info)

                            log.write(port_info + "\n")

                if open_ports:  # Show only live hosts
                    live_hosts[ip] = open_ports
                    log.write("-" * 60 + "\n")

    return live_hosts

# Read IPs/subnets from a file
def read_ip_file(file_path):
    """ Read subnets from a text file """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

if __name__ == "__main__":
    print("Select input method:")
    print("1 - Enter a single IP address")
    print("2 - Enter a subnet (e.g., 192.168.1.0/24)")
    print("3 - Read from a file (ips.txt)")
    
    choice = input("Enter your choice (1/2/3): ").strip()

    all_ips = []

    if choice == "1":
        ip = input("Enter the IP address: ").strip()
        all_ips.append(ip)

    elif choice == "2":
        subnet = input("Enter the subnet (e.g., 192.168.1.0/24): ").strip()
        all_ips.extend(generate_ips(subnet))

    elif choice == "3":
        ip_file = "ips.txt"
        subnets = read_ip_file(ip_file)
        for subnet in subnets:
            all_ips.extend(generate_ips(subnet))

    else:
        print("Invalid choice. Exiting...")
        exit()

    if not all_ips:
        print("No valid IPs found. Exiting...")
        exit()

    live_hosts = scan_network(all_ips)

    print("\nLive Hosts:")
    print("=" * 50)
    for ip, ports in live_hosts.items():
        print(f"{ip} is UP:")
        for port_info in ports:
            print(f"  {port_info}")
        print("-" * 50)
