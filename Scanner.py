import socket

class Scanner:
    def __init__(self):
        self.scan_results = []
        self.port_protocol_map = {
            20: "FTP (Data Transfer)", 21: "FTP", 22: "SSH",
            23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP"
        }

    def scan_tcp(self, target, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            result = s.connect_ex((target, port))
            if result == 0:
                protocol = self.port_protocol_map.get(port, "Sconosciuto")
                self.scan_results.append((port, protocol, "TCP", "Aperta"))
            else:
                self.scan_results.append((port, "Nessun servizio", "TCP", "Chiusa"))

    def scan_udp(self, target, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.1)
            try:
                result = s.sendto(b"", (target, port))
                self.scan_results.append((port, "Nessun servizio", "UDP", "Chiusa"))
            except Exception:
                self.scan_results.append((port, "Nessun servizio", "UDP", "Chiusa"))

    def get_results(self):
        return self.scan_results