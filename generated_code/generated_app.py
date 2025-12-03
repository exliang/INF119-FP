import json
import random
import time
from typing import List, Dict

class CyberDefender:
    def __init__(self):
        """Initialize the CyberDefender application."""
        self.system_logs = []
        self.network_traffic = []
        self.alerts = []
        self.passwords = {}
        self.encryption_key = self.generate_encryption_key()

    def generate_encryption_key(self) -> str:
        """Generate a simple encryption key."""
        return str(random.randint(100000, 999999))

    def log_system_activity(self, activity: str) -> None:
        """Log a system activity."""
        self.system_logs.append(activity)

    def monitor_network_traffic(self) -> None:
        """Monitor network traffic and log potential threats."""
        for _ in range(5):  # Simulating monitoring
            traffic = random.choice(['normal', 'malicious'])
            self.network_traffic.append(traffic)
            self.log_system_activity(f"Network traffic: {traffic}")
            self.detect_threats(traffic)
            time.sleep(1)

    def detect_threats(self, traffic: str) -> None:
        """Detect potential threats in the network traffic."""
        if traffic == 'malicious':
            self.alerts.append("Threat detected: malicious network traffic.")
            self.neutralize_threat()

    def neutralize_threat(self) -> None:
        """Neutralize the detected threat."""
        self.log_system_activity("Neutralizing threat.")
        print("Threat has been neutralized!")

    def alert_user(self) -> None:
        """Alert the user about detected threats."""
        for alert in self.alerts:
            print(f"ALERT: {alert}")

    def store_password(self, service: str, password: str) -> None:
        """Store a password securely."""
        self.passwords[service] = self.encrypt_password(password)

    def encrypt_password(self, password: str) -> str:
        """Encrypt a password using a simplistic method."""
        encrypted = ''.join(chr(ord(char) + len(self.encryption_key)) for char in password)
        return encrypted

    def retrieve_password(self, service: str) -> str:
        """Retrieve a stored password after decryption."""
        if service in self.passwords:
            return self.decrypt_password(self.passwords[service])
        return "Service not found."

    def decrypt_password(self, encrypted: str) -> str:
        """Decrypt an encrypted password."""
        decrypted = ''.join(chr(ord(char) - len(self.encryption_key)) for char in encrypted)
        return decrypted

    def run(self) -> None:
        """Run the CyberDefender application."""
        print("CyberDefender is running...")
        self.monitor_network_traffic()
        self.alert_user()

if __name__ == "__main__":
    defender = CyberDefender()
    defender.run()