# Kea2 integration example for u2_flutter
"""
Shows how to use u2_flutter with Kea2 property‑based testing.
"""
import unittest
from kea2 import precondition, prob
from u2_flutter import Flutter, with_flutter

class TestFlutterApp(unittest.TestCase):
    @prob(0.5)
    @precondition(lambda self: self.flutter.find_by_key("submit_btn").exists)
    @with_flutter
    def test_submit_button(self):
        self.flutter.find_by_key("username_input").enter_text("testuser")
        self.flutter.find_by_key("submit_btn").tap()
        greeting = self.flutter.find_by_key("greeting_text").text
        assert greeting == "Hello, testuser!"
        print("✅ Submit test passed!")

class TestHybridApp(unittest.TestCase):
    @prob(0.3)
    @precondition(lambda self: self.d(text="Open Flutter").exists)
    def test_native_navigation(self):
        self.d(text="Open Flutter").click()
        assert self.flutter.find_by_key("flutter_screen").exists
        print("✅ Hybrid navigation test passed!")

    @prob(0.3)
    @precondition(lambda self: self.flutter.find_by_key("back_btn").exists)
    @with_flutter
    def test_flutter_navigation(self):
        self.flutter.find_by_key("back_btn").tap()
        print("✅ Flutter navigation test passed!")
