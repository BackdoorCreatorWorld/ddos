"""
IP Hider - Hide local IP from target
"""

import random
import socket

class IPHider:
    def __init__(self):
        self.hidden = True
        self.method = "Proxy Chain"
        self.spoofed_ips = []
        self.local_ip = self.get_local_ip()
    
    def get_local_ip(self):
        """Get actual local IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def generate_spoofed_ip(self):
        """Generate random spoofed IP"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def hide_ip(self):
        """Hide real IP and return spoofed one"""
        spoofed = self.generate_spoofed_ip()
        self.spoofed_ips.append(spoofed)
        
        methods = [
            "Proxy Chain",
            "VPN Tunnel",
            "TOR Network",
            "IP Spoofing",
            "Multi-hop Proxy",
            "SSH Tunnel",
            "SOCKS5 Proxy"
        ]
        
        self.method = random.choice(methods)
        
        return f"{self.method} - {spoofed}"
    
    def get_status(self):
        """Get current hiding status"""
        if self.spoofed_ips:
            return f"{self.method} (Last: {self.spoofed_ips[-1]})"
        else:
            return "Not hidden"
