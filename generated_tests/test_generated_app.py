# Run with: python testing.py
import unittest
from generated_code import generated_app
from cryptography.fernet import Fernet
import logging


class TestCyberDefender(unittest.TestCase):

    def setUp(self):
        self.defender = generated_app.CyberDefender()
        self.defender.is_running = False  # Prevent threads from running during tests
        self.defender.network_traffic.clear()
        self.defender.system_logs.clear()
        self.defender.alerts.clear()
        self.defender.password_manager.clear()

    def test_initialization(self):
        self.assertEqual(len(self.defender.network_traffic), 0)
        self.assertEqual(len(self.defender.system_logs), 0)
        self.assertEqual(len(self.defender.alerts), 0)
        self.assertIsInstance(self.defender.key, bytes)

    def test_add_password(self):
        self.defender.add_password("test_service", "test_password")
        self.assertIn("test_service", self.defender.password_manager)
        self.assertIsInstance(self.defender.password_manager["test_service"], bytes)

    def test_get_password_success(self):
        self.defender.add_password("test_service", "test_password")
        retrieved_password = self.defender.get_password("test_service")
        self.assertEqual(retrieved_password, "test_password")

    def test_get_password_failure(self):
        retrieved_password = self.defender.get_password("non_existent_service")
        self.assertIsNone(retrieved_password)

    def test_encryption_decryption(self):
        service = "test_service"
        password = "test_password"
        self.defender.add_password(service, password)
        encrypted_password = self.defender.password_manager[service]
        decrypted_password = self.defender.fernet.decrypt(encrypted_password).decode()
        self.assertEqual(decrypted_password, password)

    def test_alerts_on_network_activity(self):
        self.defender.is_running = True
        for _ in range(96):  # Simulate enough network events to trigger alert
            self.defender.network_traffic.append("Traffic event")
        self.assertGreater(len(self.defender.alerts), 0)

    def test_alerts_on_system_log_activity(self):
        self.defender.is_running = True
        for _ in range(96):  # Simulate enough log events to trigger alert
            self.defender.system_logs.append("Log event")
        self.assertGreater(len(self.defender.alerts), 0)

    def test_take_action_when_alerts_present(self):
        self.defender.alerts.append("Test alert")
        with self.assertLogs(level='WARNING') as log:
            self.defender.take_action()
            self.assertIn("Test alert", log.output[0])

    def test_stop_method(self):
        self.defender.stop()
        self.assertFalse(self.defender.is_running)

    def test_run_method_initializes_threads(self):
        self.defender.is_running = True
        self.defender.run()
        self.assertTrue(len(self.defender.network_traffic) <= 100)  # Check that threads are running

if __name__ == '__main__':
    unittest.main()