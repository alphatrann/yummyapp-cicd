import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


# ================================================================
# CAP DO 1: BO TEST CO BAN
# ================================================================

class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang tinh tien don hang."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}

        result = self.app.calculate_order_total(cart)

        self.assertEqual(result, 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}

        result = self.app.calculate_order_total(cart)

        self.assertEqual(result, 95000)

    def test_calculate_total_for_empty_cart(self):
        result = self.app.calculate_order_total({})

        self.assertEqual(result, 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}

        result = self.app.calculate_order_total(cart)

        self.assertEqual(result, 0.0)


# ================================================================
# CAP DO 2: KIEM THU MA KHUYEN MAI
# ================================================================

class TestMediumLevel(unittest.TestCase):
    """Kiem thu chuc nang apply_promo_code."""

    def test_promo_code_online_valid(self):
        app = YummyApp(
            network_status="online",
            os_version=15,
        )

        result = app.apply_promo_code(100000, "GIAM10")

        self.assertEqual(result, 90000)

    def test_promo_code_offline_raises_connection_error(self):
        app = YummyApp(
            network_status="offline",
            os_version=15,
        )

        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_special_promo_code_on_os_15(self):
        app = YummyApp(
            network_status="online",
            os_version=15,
        )

        result = app.apply_promo_code(
            100000,
            "NEW_OS_ONLY",
        )

        self.assertEqual(result, 80000)

    def test_special_promo_code_on_os_14_raises_value_error(self):
        app = YummyApp(
            network_status="online",
            os_version=14,
        )

        with self.assertRaises(ValueError):
            app.apply_promo_code(
                100000,
                "NEW_OS_ONLY",
            )


# ================================================================
# CAP DO 2: KIEM THU GPS BANG MOCKING
# ================================================================

class TestHardLevel(unittest.TestCase):
    """Kiem thu get_nearby_restaurants bang mocking."""

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_location_inside_supported_area(self, mock_location):
        mock_location.return_value = (10.0, 105.0)

        app = YummyApp()

        result = app.get_nearby_restaurants()

        self.assertEqual(
            result,
            [
                "Nha hang Pho Ly Quoc Su",
                "Bun cha Huong Lien",
            ],
        )

        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_location_outside_supported_area(self, mock_location):
        mock_location.return_value = (20.0, 110.0)

        app = YummyApp()

        result = app.get_nearby_restaurants()

        self.assertEqual(result, [])

        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(self, mock_location):
        mock_location.side_effect = gps_service.GPSSignalLostError(
            "GPS signal lost"
        )

        app = YummyApp()

        result = app.get_nearby_restaurants()

        self.assertEqual(
            result,
            "Khong the xac dinh vi tri.",
        )

        mock_location.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
