# Run with: python testing.py

import unittest
import time
from unittest.mock import patch
from generated_code import generated_app

class TestCyberDefender(unittest.TestCase):

    def setUp(self):
        self.defender = generated_app.CyberDefender()
    
    def test_initialization(self):
        self.assertTrue(self.defender.is_running)
        self.assertEqual(self.defender.alerts, [])
    
    @patch('random.choice', side_effect=[True])
    def test_monitoring_alert_detection(self, mock_random):
        self.defender.start_monitoring()
        time.sleep(6)  # Wait for the alert to be generated
        self.assertIn("Threat detected! Taking action...", self.defender.alerts)
        self.defender.stop_monitoring()

    @patch('random.choice', side_effect=[False])
    def test_monitoring_no_alerts(self, mock_random):
        self.defender.start_monitoring()
        time.sleep(6)  # Ensure no alerts are generated
        self.assertEqual(self.defender.alerts, [])
        self.defender.stop_monitoring()

    @patch('generated_app.EncryptionTool.encrypt', return_value='drowssap')
    def test_encrypt_data(self, mock_encrypt):
        encrypted_data = self.defender.encrypt_data('password')
        self.assertEqual(encrypted_data, 'drowssap')

    @patch('generated_app.EncryptionTool.decrypt', return_value='password')
    def test_decrypt_data(self, mock_decrypt):
        decrypted_data = self.defender.decrypt_data('drowssap')
        self.assertEqual(decrypted_data, 'password')

    def test_store_password(self):
        self.defender.store_password('service1', 'user1', 'pass1')
        self.assertIn('service1', self.defender.pwd_manager.passwords)
        self.assertEqual(self.defender.pwd_manager.passwords['service1']['user1'], 'pass1')

    def test_store_multiple_passwords(self):
        self.defender.store_password('service1', 'user1', 'pass1')
        self.defender.store_password('service1', 'user2', 'pass2')
        self.assertEqual(self.defender.pwd_manager.passwords['service1']['user2'], 'pass2')

    def test_store_different_services(self):
        self.defender.store_password('service1', 'user1', 'pass1')
        self.defender.store_password('service2', 'user1', 'pass2')
        self.assertIn('service1', self.defender.pwd_manager.passwords)
        self.assertIn('service2', self.defender.pwd_manager.passwords)

    @patch('generated_app.CyberDefender.take_action')
    def test_take_action_on_threat(self, mock_take_action):
        self.defender.alerts.append("Threat detected! Taking action...")
        self.defender.take_action()
        mock_take_action.assert_called_once()

    def test_stop_monitoring(self):
        self.defender.stop_monitoring()
        self.assertFalse(self.defender.is_running)

    def test_no_alerts_after_stop(self):
        self.defender.start_monitoring()
        self.defender.stop_monitoring()
        time.sleep(6)  # Ensure time for monitoring to end
        self.assertEqual(self.defender.alerts, [])

if __name__ == '__main__':
    unittest.main()