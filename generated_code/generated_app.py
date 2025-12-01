import json
import logging
import random
import time
from cryptography.fernet import Fernet  # This is an external package

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CyberDefender:
    def __init__(self):
        self.alerts = []
        self.user_data = {}
        self.encryption_key = self.generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)

    def generate_encryption_key(self):
        """Generates a new key for encryption."""
        return Fernet.generate_key()

    def encrypt_data(self, data):
        """
        Encrypts data using Fernet symmetric encryption.
        
        :param data: The data to encrypt.
        :return: The encrypted data.
        """
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        """
        Decrypts data using Fernet symmetric encryption.
        
        :param encrypted_data: The data to decrypt.
        :return: The decrypted data.
        """
        return self.fernet.decrypt(encrypted_data).decode()

    def monitor_network_traffic(self):
        """Simulate monitoring of network traffic."""
        logging.info("Monitoring network traffic...")
        time.sleep(2)  # Simulate delay
        suspicious_activity = random.choice([True, False])
        if suspicious_activity:
            self.handle_alert("Suspicious activity detected in network traffic.")

    def monitor_system_logs(self):
        """Simulate monitoring of system logs."""
        logging.info("Monitoring system logs...")
        time.sleep(2)  # Simulate delay
        malware_detected = random.choice([True, False])
        if malware_detected:
            self.handle_alert("Malware detected in system logs.")

    def handle_alert(self, message):
        """
        Handle a security alert by logging it and taking action.
        
        :param message: The alert message.
        """
        logging.warning(message)
        self.alerts.append(message)
        self.take_action(message)

    def take_action(self, message):
        """Take necessary actions based on the alert message."""
        logging.info("Taking action for alert: {}".format(message))

    def add_user_data(self, username, password):
        """
        Adds user credentials and encrypts them.
        
        :param username: The user's username.
        :param password: The user's password.
        """
        encrypted_password = self.encrypt_data(password)
        self.user_data[username] = encrypted_password
        logging.info(f"Password for {username} stored securely.")

    def retrieve_password(self, username):
        """
        Retrieves and decrypts the user's password.
        
        :param username: The user's username.
        :return: The decrypted password.
        """
        encrypted_password = self.user_data.get(username)
        if encrypted_password:
            return self.decrypt_data(encrypted_password)
        else:
            logging.error("Username not found.")
            return None

    def run(self):
        """Executes the monitoring process."""
        while True:
            self.monitor_network_traffic()
            self.monitor_system_logs()
            time.sleep(10)  # Run monitoring every 10 seconds

if __name__ == "__main__":
    cyber_defender = CyberDefender()
    cyber_defender.add_user_data("user1", "secure_password_123")
    password = cyber_defender.retrieve_password("user1")
    if password:
        logging.info(f"Retrieved password for user1: {password}")
    cyber_defender.run()