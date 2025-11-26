# Run with: python testing.py
import unittest
from generated_code import generated_app
import time

class TestCyberDefender(unittest.TestCase):

    def setUp(self):
        self.cyber_defender = generated_app.CyberDefender()

    def test_initial_alerts_empty(self):
        self.assertEqual(self.cyber_defender.alerts, [])

    def test_initial_passwords_empty(self):
        self.assertEqual(self.cyber_defender.passwords, {})

    def test_add_password(self):
        self.cyber_defender.add_password("service1", "password123")
        self.assertIn("service1", self.cyber_defender.passwords)

    def test_get_password(self):
        self.cyber_defender.add_password("service2", "mysecret")
        retrieved_password = self.cyber_defender.get_password("service2")
        self.assertEqual(retrieved_password, "mysecret")

    def test_encrypt_password(self):
        encrypted = self.cyber_defender.encrypt_password("mypassword")
        self.assertNotEqual(encrypted, "mypassword")

    def test_decrypt_password(self):
        encrypted = self.cyber_defender.encrypt_password("mypassword")
        decrypted = self.cyber_defender.decrypt_password(encrypted)
        self.assertEqual(decrypted, "mypassword")

    def test_detect_threat(self):
        # Mocking the detect_threat function to always return True
        self.cyber_defender.detect_threat = lambda: True
        self.cyber_defender.alert_threat()
        self.assertEqual(len(self.cyber_defender.alerts), 1)
        self.assertEqual(self.cyber_defender.alerts[0], "Threat detected!")

    def test_alert_threat(self):
        # Reset alerts and call alert_threat
        self.cyber_defender.alerts.clear()
        self.cyber_defender.alert_threat()
        self.assertEqual(len(self.cyber_defender.alerts), 1)

    def test_start_monitoring_creates_thread(self):
        self.cyber_defender.start_monitoring()
        self.assertIsNotNone(self.cyber_defender.monitoring_thread)
        self.assertTrue(self.cyber_defender.monitoring_thread.is_alive())

    def test_take_action_called_on_alert(self):
        self.cyber_defender.take_action = lambda: print("Action taken")  # Mocking take_action
        self.cyber_defender.detect_threat = lambda: True  # Force a threat detection
        self.cyber_defender.alert_threat()

    def test_get_password_nonexistent_service(self):
        result = self.cyber_defender.get_password("nonexistent")
        self.assertIsNone(result)

    def test_multiple_threads_not_started(self):
        self.cyber_defender.start_monitoring()
        previous_thread_id = self.cyber_defender.monitoring_thread.ident
        self.cyber_defender.start_monitoring()  # Should not start a new thread
        self.assertEqual(previous_thread_id, self.cyber_defender.monitoring_thread.ident)

if __name__ == '__main__':
    unittest.main()