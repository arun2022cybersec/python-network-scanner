import socket
import subprocess
from tabulate import tabulate
import os
import time

class NetworkScanner:
    def __init__(self, target_ip=None):
        self.target_ip = target_ip if target_ip else socket.gethostbyname(socket.gethostname())
        self.results = []

    def scan_port(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((self.target_ip, port))
        s.close()
        return result == 0

    def identify_service(self, port):
        try:
            result = subprocess.check_output(['lsof', '-i', f':{port}'], stderr=subprocess.DEVNULL)
            service_name = result.decode().split('\n')[1].split()[0]
            return service_name
        except (IndexError, subprocess.CalledProcessError):
            return "Unknown"

    def scan_network(self, start_port=1, end_port=65535):
        for port in range(start_port, end_port + 1):
            if self.scan_port(port):
                service = self.identify_service(port)
                result = {
                    'Port': port,
                    'Status': 'Open',
                    'Listening': 'Yes',
                    'Service': service
                }
                yield result

    def perform_scan(self, start_port=1, end_port=65535):
        headers = ["Port", "Status", "Listening", "Service"]
        print(tabulate([], headers, tablefmt="grid"))
        for result in self.scan_network(start_port, end_port):
            self.results.append([result['Port'], result['Status'], result['Listening'], result['Service']])
            os.system('clear')  # Clear the terminal output
            print(tabulate(self.results, headers=headers, tablefmt="grid"))
            time.sleep(0.1)  # Add a small delay to make the output more readable

if __name__ == "__main__":
    scanner = NetworkScanner()  # For localhost
    # scanner = NetworkScanner("192.168.1.1")  # For a specified IP
    scanner.perform_scan()
