# Run with: python testing.py
import unittest
from generated_code import generated_app

class TestCyberDefender(unittest.TestCase):
    def setUp(self):
        self.defender = generated_app.CyberDefender()

    def test_initial_conditions(self):
        self.assertEqual(len(self.defender.network_traffic), 0)
        self.assertEqual(len(self.defender.system_logs), 0)
        self.assertEqual(len(self.defender.alerts), 0)
        self.assertEqual(len(self.defender.passwords), 0)
        self.assertTrue(self.defender.running)

    def test_add_valid_password(self):
        self.defender.add_password("email", "password123")
        self.assertIn("email", self.defender.passwords)
        self.assertEqual(self.defender.passwords["email"], "qbtbnqsf124")

    def test_add_invalid_password_short(self):
        with self.assertRaises(ValueError):
            self.defender.add_password("email", "pass")

    def test_add_invalid_password_no_digits(self):
        with self.assertRaises(ValueError):
            self.defender.add_password("email", "password")

    def test_validate_password_valid(self):
        self.assertTrue(self.defender.validate_password("password123"))
        self.assertTrue(self.defender.validate_password("passw0rd"))

    def test_validate_password_invalid_short(self):
        self.assertFalse(self.defender.validate_password("short"))

    def test_validate_password_invalid_no_digits(self):
        self.assertFalse(self.defender.validate_password("password"))

    def test_encrypt_password(self):
        encrypted = self.defender.encrypt_password("password123")
        self.assertEqual(encrypted, "qbtbnqsf124")

    def test_simulate_network_traffic(self):
        traffic = self.defender.simulate_network_traffic()
        self.assertIn("source", traffic)
        self.assertIn("destination", traffic)
        self.assertIn("data", traffic)
        self.assertEqual(len(traffic["data"]), 10)

    def test_detect_threat_no_threat(self):
        self.defender.detect_threats({"source": "1.1.1.1", "data": "safe_data"})
        self.assertEqual(len(self.defender.alerts), 0)

    def test_detect_threat_with_threat(self):
        self.defender.detect_threats({"source": "1.1.1.1", "data": "malware_present"})
        self.assertEqual(len(self.defender.alerts), 1)
        self.assertIn("Threat detected from 1.1.1.1!", self.defender.alerts)

    def test_neutralize_threat_logging(self):
        with self.assertLogs('root', level='INFO') as log:
            self.defender.neutralize_threat({"source": "2.2.2.2"})
            self.assertIn("Neutralizing threat from 2.2.2.2.", log.output[0])

    def test_stop_functionality(self):
        self.defender.stop()
        self.assertFalse(self.defender.running)

if __name__ == '__main__':
    unittest.main()