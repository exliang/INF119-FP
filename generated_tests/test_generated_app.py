# Run with: python testing.py
import unittest
from generated_code import generated_app

class TestCyberDefender(unittest.TestCase):
    
    def setUp(self):
        self.cyber_defender = generated_app.CyberDefender()
    
    def test_generate_encryption_key(self):
        key = self.cyber_defender.generate_encryption_key()
        self.assertIsNotNone(key)
        self.assertEqual(len(key), 44)  # Fernet key length

    def test_encrypt_data(self):
        data = "my_secret_password"
        encrypted_data = self.cyber_defender.encrypt_data(data)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(encrypted_data.decode(), data)

    def test_decrypt_data(self):
        data = "my_secret_password"
        encrypted_data = self.cyber_defender.encrypt_data(data)
        decrypted_data = self.cyber_defender.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, data)

    def test_add_user_data(self):
        self.cyber_defender.add_user_data("user1", "password1")
        self.assertIn("user1", self.cyber_defender.user_data)
    
    def test_retrieve_password(self):
        self.cyber_defender.add_user_data("user2", "password2")
        retrieved_password = self.cyber_defender.retrieve_password("user2")
        self.assertEqual(retrieved_password, "password2")

    def test_retrieve_non_existent_password(self):
        retrieved_password = self.cyber_defender.retrieve_password("non_existent_user")
        self.assertIsNone(retrieved_password)

    def test_handle_alert(self):
        self.cyber_defender.handle_alert("Test alert")
        self.assertIn("Test alert", self.cyber_defender.alerts)

    def test_monitor_network_traffic(self):
        # This test needs to be deterministic, so we need to mock the randomness.
        # We cannot directly test logging output, focus on alerts instead.
        self.cyber_defender.monitor_network_traffic()
        self.assertLessEqual(len(self.cyber_defender.alerts), 1)  # May get 0 or 1

    def test_monitor_system_logs(self):
        self.cyber_defender.monitor_system_logs()
        self.assertLessEqual(len(self.cyber_defender.alerts), 1)  # May get 0 or 1

    def test_take_action(self):
        with self.assertLogs(level='INFO') as log:
            self.cyber_defender.take_action("Test action")
            self.assertIn("Taking action for alert: Test action", log.output[0])

if __name__ == '__main__':
    unittest.main()