"""
Cloudflare Bypass Module
"""

import requests
import re
import random
from urllib.parse import urlparse

class CloudflareBypass:
    def __init__(self):
        self.methods = [
            "Header Injection",
            "Real IP Discovery",
            "Cookie Bypass",
            "JavaScript Challenge Solver",
            "Direct IP Attack"
        ]
    
    def check(self, url):
        """Check if site is protected by Cloudflare"""
        result = {
            'protected': False,
            'method': None
        }
        
        try:
            response = requests.get(url, timeout=5)
            headers = response.headers
            
            # Check Cloudflare headers
            if 'cf-ray' in headers:
                result['protected'] = True
                result['method'] = random.choice(self.methods)
            elif 'cloudflare' in response.text.lower():
                result['protected'] = True
                result['method'] = random.choice(self.methods)
            elif 'cf-browser-verification' in response.text:
                result['protected'] = True
                result['method'] = random.choice(self.methods)
                
        except:
            pass
        
        return result
    
    def bypass_headers(self):
        """Generate Cloudflare bypass headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'CF-Connecting-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        
        return headers
