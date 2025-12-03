import json
import logging
import threading
import time
import random
import string

class CyberDefender:
    def __init__(self):
        self.network_traffic = []
        self.system_logs = []
        self.alerts = []
        self.passwords = {}
        self.running = True
        logging.basicConfig(level=logging.INFO)

    def monitor_traffic(self):
        while self.running:
            traffic = self.simulate_network_traffic()
            self.network_traffic.append(traffic)
            self.detect_threats(traffic)
            time.sleep(2)

    def simulate_network_traffic(self):
        return {
            "source": f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "destination": f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "data": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        }

    def detect_threats(self, traffic):
        if "malware" in traffic["data"]:
            self.alert_user(f"Threat detected from {traffic['source']}!")
            self.neutralize_threat(traffic)

    def alert_user(self, message):
        logging.info(message)
        self.alerts.append(message)

    def neutralize_threat(self, traffic):
        logging.info(f"Neutralizing threat from {traffic['source']}.")

    def add_password(self, name, password):
        if not self.validate_password(password):
            raise ValueError("Password does not meet security criteria.")
        self.passwords[name] = self.encrypt_password(password)

    def validate_password(self, password):
        return len(password) >= 8 and any(c.isdigit() for c in password)

    def encrypt_password(self, password):
        return ''.join(chr(ord(c) + 1) for c in password)

    def stop(self):
        self.running = False

def main():
    defender = CyberDefender()
    
    traffic_monitor_thread = threading.Thread(target=defender.monitor_traffic)
    traffic_monitor_thread.start()

    # Simulate adding passwords
    try:
        defender.add_password("email", "password123")
    except ValueError as e:
        logging.error(e)

    time.sleep(10)  # Run for 10 seconds
    defender.stop()
    traffic_monitor_thread.join()
    
    # Save alerts to a file
    with open('alerts.json', 'w') as f:
        json.dump(defender.alerts, f)

if __name__ == "__main__":
    main()