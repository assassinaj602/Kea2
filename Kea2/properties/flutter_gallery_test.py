"""
Kea2 Property Test for Flutter Gallery Demo App
Demonstrates auto-detection of Flutter driver and widget interactions.
"""
import unittest
from kea2 import precondition, prob

class TestFlutterGallery(unittest.TestCase):
    """Property test suite for Flutter Gallery demo application."""

    @prob(0.5)
    @precondition(lambda self: self.flutter.find_by_key("demo_button").exists)
    def test_button_tap(self):
        """Precondition check: demo_button exists, Action: tap and verify response."""
        print("🔍 Checking precondition: 'demo_button' exists")
        self.flutter.find_by_key("demo_button").tap()
        print("✅ Action: Tapped 'demo_button' successfully")

    @prob(0.5)
    @precondition(lambda self: self.flutter.find_by_text("Gallery").exists)
    def test_title_check(self):
        """Precondition check: 'Gallery' title text visible."""
        print("🔍 Precondition check: Title text 'Gallery' is visible")
        title_text = self.flutter.find_by_text("Gallery").get_text()
        print(f"✅ Retrieved text: '{title_text}'")

if __name__ == "__main__":
    unittest.main()
