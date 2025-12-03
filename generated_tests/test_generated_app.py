# Run with: python testing.py
import unittest
from generated_code import generated_app

class TestCyberDefender(unittest.TestCase):
    def setUp(self):
        self.defender = generated_app.CyberDefender()

    def test_initialization(self):
        self.assertEqual(len(self.defender.system_logs), 0)
        self.assertEqual(len(self.defender.network_traffic), 0)
        self.assertEqual(len(self.defender.alerts), 0)
        self.assertEqual(len(self.defender.passwords), 0)

    def test_generate_encryption_key(self):
        key1 = self.defender.encryption_key
        key2 = self.defender.generate_encryption_key()  # Method call should reset the key
        self.assertNotEqual(key1, key2)

    def test_log_system_activity(self):
        self.defender.log_system_activity("Test activity")
        self.assertIn("Test activity", self.defender.system_logs)

    def test_detect_threats_malicious(self):
        self.defender.detect_threats('malicious')
        self.assertIn("Threat detected: malicious network traffic.", self.defender.alerts)

    def test_detect_threats_normal(self):
        self.defender.detect_threats('normal')
        self.assertNotIn("Threat detected: malicious network traffic.", self.defender.alerts)

    def test_neutralize_threat_logs_activity(self):
        self.defender.detect_threats('malicious')
        self.assertIn("Neutralizing threat.", self.defender.system_logs)

    def test_store_password(self):
        self.defender.store_password("test_service", "test_password")
        self.assertIn("test_service", self.defender.passwords)

    def test_encryption_decryption(self):
        self.defender.store_password("test_service", "test_password")
        encrypted_password = self.defender.passwords["test_service"]
        decrypted_password = self.defender.decrypt_password(encrypted_password)
        self.assertEqual(decrypted_password, "test_password")

    def test_retrieve_nonexistent_password(self):
        result = self.defender.retrieve_password("nonexistent_service")
        self.assertEqual(result, "Service not found.")

    def test_retrieve_existing_password(self):
        self.defender.store_password("test_service", "test_password")
        result = self.defender.retrieve_password("test_service")
        self.assertEqual(result, "test_password")

    def test_monitor_network_traffic_detects_malicious(self):
        self.defender.network_traffic = ['normal', 'malicious', 'normal', 'normal', 'malicious']
        for traffic in self.defender.network_traffic:
            self.defender.detect_threats(traffic)
        self.assertGreater(len(self.defender.alerts), 0)

    def test_alert_user_when_threats_detected(self):
        self.defender.detect_threats('malicious')
        with self.assertLogs(level='INFO') as log:
            self.defender.alert_user()
            self.assertIn("ALERT: Threat detected: malicious network traffic.", log.output)

if __name__ == '__main__':
    unittest.main()