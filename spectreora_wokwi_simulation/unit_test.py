import unittest
from unittest.mock import Mock, patch
import main


class TestMain(unittest.TestCase):

    def test_wifi_connect_success(self):
        # Test that the wifi_connect function successfully connects to the specified Wi-Fi network
        mock_wlan = Mock()
        mock_sta_if = Mock(return_value=mock_wlan)
        with patch('main.WLAN', mock_sta_if):
            mock_wlan.isconnected.return_value = True
            mock_wlan.ifconfig.return_value = (
                '192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
            result = main.wifi_connect()
            self.assertEqual(result, mock_wlan)
            mock_sta_if.assert_called_once()
            mock_wlan.active.assert_called_once_with(True)
            mock_wlan.connect.assert_called_once_with(
                main.config.SSID, main.config.PASSWORD)
            mock_wlan.ifconfig.assert_called_once()

    def test_read_adc(self):
        # Test that the read_adc function collects ECG data correctly
        mock_adc = Mock()
        mock_pin = Mock(return_value=mock_adc)
        with patch('main.Pin', mock_pin):
            mock_adc.read_u16.return_value = 500
            # Test filling the ecg_data_array
            for i in range(3000):
                result = main.read_adc(mock_adc)
                if i < 2999:
                    self.assertFalse(result)
                else:
                    self.assertTrue(result)
            # Test resetting the ecg_data_array
            self.assertEqual(main.ecg_data_array, [None] * 3000)

    def test_send_data(self):
        # Test that the send_data function sends data correctly
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post = Mock(return_value=mock_response)
        with patch('main.urequests.post', mock_post):
            result = main.send_data(
                Mock(), 'http://example.com', '{}', {'Content-Type': 'application/json'})
            self.assertEqual(result, 200)
            mock_post.assert_called_once_with(
                'http://example.com', data='{}', headers={'Content-Type': 'application/json'})
