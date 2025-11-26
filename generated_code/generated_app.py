import json
import threading
import time
import random
from cryptography.fernet import Fernet

class CyberDefender:
    def __init__(self):
        self.alerts = []
        self.passwords = {}
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.monitoring_thread = None

    def start_monitoring(self):
        """Starts monitoring network traffic and system logs."""
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.monitoring_thread = threading.Thread(target=self.monitor, daemon=True)
            self.monitoring_thread.start()
    
    def monitor(self):
        """Simulates monitoring of traffic and logs for suspicious activities."""
        while True:
            time.sleep(random.randint(1, 3))  # Simulate random monitoring intervals
            if self.detect_threat():
                self.alert_threat()

    def detect_threat(self):
        """Simulates threat detection. Returns True if a threat is detected."""
        return random.choice([True, False])
    
    def alert_threat(self):
        """Handles alerting on detected threats."""
        alert_message = "Threat detected!"
        self.alerts.append(alert_message)
        print(alert_message)
        self.take_action()

    def take_action(self):
        """Simulates taking necessary actions to neutralize threats."""
        print("Taking necessary actions to neutralize the threat...")
    
    def add_password(self, service, password):
        """Adds a password for a specific service."""
        self.passwords[service] = self.encrypt_password(password)
    
    def get_password(self, service):
        """Retrieves a decrypted password for a specific service."""
        return self.decrypt_password(self.passwords[service]) if service in self.passwords else None

    def encrypt_password(self, password):
        """Encrypts a password using the encryption key."""
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        """Decrypts a password using the encryption key."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()

def main():
    cyber_defender = CyberDefender()
    
    cyber_defender.start_monitoring()
    
    # Simulate adding passwords
    cyber_defender.add_password("email", "mysecretpassword")
    print("Password for email:", cyber_defender.get_password("email"))
    
    # Let the monitoring run for a while
    time.sleep(10)

if __name__ == "__main__":
    main()