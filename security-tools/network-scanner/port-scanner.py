import nmap
import ipaddress

def generate_ips(subnet):
    """ Generate all IP addresses within a given subnet """
    try:
        network = ipaddress.ip_network(subnet, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        print(f"Invalid subnet: {subnet}")
        return []

def scan_network(ip_list, ports="22,80,443,3306,5432,6379,27017,9200,9090"):
    """ Scan each IP in the list and display only those that are up """
    scanner = nmap.PortScanner()
    live_hosts = {}
    
    for ip in ip_list:
        print(f"Scanning {ip} ...")
        scanner.scan(ip, arguments=f'-Pn -p {ports}')  # Scan for specific ports
        
        if ip in scanner.all_hosts():
            open_ports = []
            for proto in scanner[ip].all_protocols():
                for port in scanner[ip][proto]:
                    state = scanner[ip][proto][port]['state']
                    service = scanner[ip][proto][port].get('name', 'unknown')
                    if state == 'open':
                        open_ports.append(f"Port {port}: {service}")
            
            if open_ports:  # Display only hosts with at least one open port
                live_hosts[ip] = open_ports
    
    return live_hosts

def read_ip_file(file_path):
    """ Read subnets from file """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    ip_file = "ips.txt"  # Input file containing subnets (e.g. 192.168.0.1/28)
    subnets = read_ip_file(ip_file)
    
    all_ips = []
    for subnet in subnets:
        all_ips.extend(generate_ips(subnet))
    
    live_hosts = scan_network(all_ips)
    
    print("\nLive Hosts:")
    print("=" * 50)
    for ip, ports in live_hosts.items():
        print(f"{ip} is UP:")
        for port_info in ports:
            print(f"  {port_info}")
        print("-" * 50)
