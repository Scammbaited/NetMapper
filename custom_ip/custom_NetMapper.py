import netifaces
import ipaddress
from scapy.all import ARP, Ether, srp, sr, IP, TCP
import requests
from bs4 import BeautifulSoup
from socket import gethostbyaddr, herror

def get_network_range_from_file(filename):
    with open(filename, 'r') as file:
        network_range = file.read().strip()
    return network_range

def get_active_ips(network_range):
    print("Preparing to send ARP requests...")
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network_range)
    print("Sending ARP requests...")
    answered, _ = srp(arp_request, timeout=5, verbose=0)
    print("Processing responses...")
    active_ips = [packet[1].psrc for packet in answered]

    return active_ips

def get_hostname(ip):
    try:
        hostname, _, _ = gethostbyaddr(ip)
    except herror:
        hostname = 'Unknown'
    return hostname

def read_ports_from_file(filename):
    with open(filename, 'r') as file:
        ports = [int(line.strip()) for line in file]
    return ports

def get_open_ports(ip, ports):
    print(f"Preparing packets for {ip}...")
    packets = IP(dst=ip) / TCP(dport=ports, flags="S")

    print(f"Sending packets to {ip}...")
    answered, _ = sr(packets, timeout=2, verbose=0)

    print(f"Processing responses from {ip}...")
    open_ports = [packet[1][TCP].sport for packet in answered]

    return open_ports

def get_service(port):
    services = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        80: 'HTTP',
        443: 'HTTPS'
    }
    return services.get(port, 'Unknown')

def get_website_title(ip, port):
    url = f"http://{ip}:{port}"
    try:
        response = requests.get(url, timeout=3)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string if soup.title else "No title tag found"
    except requests.exceptions.RequestException:
        print(f"Unable to fetch the website title for {ip}:{port}.")
        return "Unable to fetch title"

def get_smb_shares(ip, ports):
    print(f"Checking for SMB shares on {ip}...")
    return 445 in ports

def create_html(network_map):
    body = ""
    for ip, info in network_map.items():
        body += f"""
        <div class="card mb-4">
            <div class="card-header">
                <h2>{ip} - {info['Hostname']}</h2>
            </div>
            <div class="card-body">
                <h5 class="card-title">Open Ports:</h5>
                <p class="card-text">{info['Open Ports']}</p>
                <h5 class="card-title">Website Title:</h5>
                <p class="card-text">{info['Website Title']}</p>
                <h5 class="card-title">SMB Shares:</h5>
                <p class="card-text">{'Yes' if info['SMB Shares'] else 'No'}</p>
            </div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Network Map Custom IP</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {{
                background: #f5f5f5;
                font-family: Arial, sans-serif;
            }}
            .card {{
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                transition: 0.3s;
            }}
            .card:hover {{
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
            }}
            .container {{
                max-width: 700px;
                margin: auto;
                padding: 20px;
            }}
            .card-header {{
                font-size: 20px;
                font-weight: bold;
            }}
            .card-text {{
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5 mb-5 text-center">Network Map Custom IP</h1>
            {body}
        </div>
    </body>
    </html>
    """

    with open("network_map.html", "w") as file:
        file.write(html_content)

if __name__ == "__main__":
    default_network_range = get_network_range_from_file('ip.txt')
    print(f"Network range is {default_network_range}.")

    print("Scanning for active IPs...")
    active_ips = get_active_ips(default_network_range)
    print("Active IPs:")
    for ip in active_ips:
        print(ip)

    ports = read_ports_from_file('ports.txt')

    network_map = {}
    for ip in active_ips:
        hostname = get_hostname(ip)
        print(f"Scanning {ip} ({hostname}) for open ports...")
        open_ports = get_open_ports(ip, ports)
        network_map[ip] = {'Hostname': hostname, 'Open Ports': {}, 'Website Title': None, 'SMB Shares': None}
        for port in open_ports:
            service = get_service(port)
            network_map[ip]['Open Ports'][port] = service
            if service in ['HTTP', 'HTTPS']:
                network_map[ip]['Website Title'] = get_website_title(ip, port)
        network_map[ip]['SMB Shares'] = get_smb_shares(ip, open_ports)

    print("Network Map:")
    for ip, info in network_map.items():
        print(f"{ip} ({info['Hostname']}):")
        print(f"  Open Ports: {info['Open Ports']}")
        print(f"  Website Title: {info['Website Title']}")
        print(f"  SMB Shares: {'Yes' if info['SMB Shares'] else 'No'}")

    print("Creating HTML file...")
    create_html(network_map)
    print("HTML file created.")
