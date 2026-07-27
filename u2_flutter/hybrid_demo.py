"""
Hybrid Demo: Native Android + Flutter together
Simplified version that works on ANY Android phone!
"""
import uiautomator2 as u2
from u2_flutter import Flutter
import time

# Connect to device
d = u2.connect()
print("✅ Connected to device!")

# Create Flutter driver
flutter = Flutter(d)
print("🔄 Attaching Flutter driver...")
flutter.attach()
print("✅ Flutter driver attached!")

print("\n" + "="*50)
print("HYBRID DEMO: Native + Flutter")
print("="*50)

# STEP 1: Native Android - Press Home
print("\n📱 Step 1: Native Android - Press Home")
d.press("home")
time.sleep(1)
print("✅ Native: Pressed Home")

# STEP 2: Native Android - Press Recent Apps (shows native UI)
print("\n📱 Step 2: Native Android - Press Recent Apps")
d.press("recent")
time.sleep(1)
print("✅ Native: Recent Apps shown")
d.press("home")
time.sleep(1)
print("✅ Native: Back to Home")

# STEP 3: Native Android - Open Quick Settings
print("\n📱 Step 3: Native Android - Open Quick Settings")
d.open_quick_settings()
time.sleep(2)
print("✅ Native: Quick Settings opened")
d.press("back")
time.sleep(1)
print("✅ Native: Quick Settings closed")

# STEP 4: Launch Flutter app
print("\n📱 Step 4: Launch Flutter app")
d.app_start("com.example.test_app")
time.sleep(3)
print("✅ Flutter app launched")

# STEP 5: Flutter action - Tap submit button
print("\n📱 Step 5: Flutter - Tap submit button")
flutter.find_by_key("submit_btn").tap()
time.sleep(1)
print("✅ Flutter: Button tapped")

# STEP 6: Flutter action - Read greeting
print("\n📱 Step 6: Flutter - Read greeting")
greeting = flutter.find_by_key("greeting_text").text
print(f"✅ Flutter: Greeting = '{greeting}'")

# STEP 7: Native Android - Press Home again
print("\n📱 Step 7: Native Android - Press Home")
d.press("home")
time.sleep(1)
print("✅ Native: Back to Home")

print("\n" + "="*50)
print("🎉 HYBRID DEMO COMPLETE!")
print("   Native actions ✅ + Flutter actions ✅")
print("="*50)

# Clean up
print("\n🔄 Detaching Flutter driver...")
flutter.detach()
print("✅ Detached!")

input("\nPress Enter to exit...")