# Run with: python testing.py

import unittest
from generated_code import generated_app
from cryptography.fernet import InvalidToken

class TestCyberDefender(unittest.TestCase):

    def setUp(self):
        self.defender = generated_app.CyberDefender()

    def test_generate_key(self):
        self.assertIsNotNone(self.defender.encryption_key)
        self.assertEqual(len(self.defender.encryption_key), 44)  # Fernet key length

    def test_encrypt_data(self):
        data = "my_secret_password"
        encrypted_data = self.defender.encrypt_data(data)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(data.encode(), encrypted_data)

    def test_decrypt_data(self):
        data = "my_secret_password"
        encrypted_data = self.defender.encrypt_data(data)
        decrypted_data = self.defender.decrypt_data(encrypted_data)
        self.assertEqual(data, decrypted_data)

    def test_detect_threat(self):
        self.defender.detect_threat("Malware detected")
        self.assertIn("Malware detected", self.defender.alerts)
        self.assertIn("Malware detected", self.defender.logs)

    def test_alert_user(self):
        self.defender.detect_threat("Virus detected")
        with self.assertLogs(level='INFO') as log:
            self.defender.alert_user()
        self.assertIn("Alert: Virus detected", log.output[0])

    def test_add_password(self):
        self.defender.add_password("test_service", "password123")
        self.assertIn("test_service", self.defender.passwords)

    def test_get_password(self):
        self.defender.add_password("test_service", "password123")
        password = self.defender.get_password("test_service")
        self.assertEqual(password, "password123")

    def test_get_password_not_found(self):
        with self.assertRaises(ValueError):
            self.defender.get_password("non_existent_service")

    def test_logs_after_event(self):
        self.defender.detect_threat("Unauthorized access")
        self.assertEqual(len(self.defender.logs), 1)
        self.assertEqual(self.defender.logs[0], "Unauthorized access")

    def test_save_logs(self):
        self.defender.detect_threat("Test log save")
        filename = "test_logs.json"
        self.defender.save_logs(filename)
        with open(filename, 'r') as f:
            logs = json.load(f)
        self.assertIn("Test log save", logs)

if __name__ == '__main__':
    unittest.main()