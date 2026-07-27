# Basic usage example for u2_flutter
"""
Shows how to find and interact with Flutter widgets.
"""
import uiautomator2 as u2
from u2_flutter import Flutter, with_flutter

def basic_usage():
    d = u2.connect()
    flutter = Flutter(d)
    flutter.find_by_key("submit_btn").tap()
    text = flutter.find_by_key("greeting_text").text
    print(f"Greeting: {text}")
    flutter.find_by_key("username_input").enter_text("testuser")


def with_decorator():
    class Test:
        @with_flutter
        def test(self):
            self.flutter.find_by_key("username_input").enter_text("testuser")
            self.flutter.find_by_key("submit_btn").tap()
            assert self.flutter.find_by_key("greeting_text").text == "Hello, testuser!"
            print("✅ Test passed!")
    Test().test()

if __name__ == "__main__":
    basic_usage()
