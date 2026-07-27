import uiautomator2 as u2
from u2_flutter import Flutter
import time

# Connect to device
d = u2.connect()
print("✅ Connected to device!")

# Create and attach Flutter driver manually
flutter = Flutter(d)
print("🔄 Attaching Flutter driver...")
flutter.attach()
print("✅ Flutter driver attached!")

# Wait a moment for connection to stabilize
time.sleep(1)

print("\n🔍 Finding submit button...")
submit_btn = flutter.find_by_key("submit_btn")
print("✅ Found submit button!")

print("👆 Tapping submit button...")
submit_btn.tap()
print("✅ Tapped submit button!")

# Wait for UI to update
time.sleep(0.5)

print("📖 Getting greeting text...")
greeting = flutter.find_by_key("greeting_text").text
print(f"✅ Greeting text: '{greeting}'")

# Detach when done
print("\n🔄 Detaching Flutter driver...")
flutter.detach()
print("✅ Detached!")

print("\n🎉 Demo completed successfully!")

# Keep window open
input("\nPress Enter to exit...")