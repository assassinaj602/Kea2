import time
import os
import sys
import logging
import uiautomator2 as u2

# Add parent directory to sys.path so we can import u2_flutter locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from u2_flutter import with_flutter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class U2FlutterBenchmark:
    def __init__(self):
        print("Connecting to Android device via uiautomator2...")
        self.d = u2.connect()
        # Force start package
        self.d.app_start("com.example.test_app", stop=True)
        time.sleep(3)

    @with_flutter()
    def run_benchmark(self):
        print("=== u2_flutter Driver Benchmark ===")
        
        # Connection duration is handled internally in the decorator, 
        # but let's measure direct interactions to compare action roundtimes.
        
        # 1. Find Element 'submit_btn'
        print("Finding submit_btn...")
        start_find = time.perf_counter()
        submit_btn = self.flutter.find_by_key("submit_btn")
        find_duration = time.perf_counter() - start_find
        print(f"submit_btn found/prepared in: {find_duration:.4f}s")
        
        # 2. Tap Element
        print("Tapping submit_btn...")
        start_tap = time.perf_counter()
        submit_btn.tap()
        tap_duration = time.perf_counter() - start_tap
        print(f"Tap completed in: {tap_duration:.4f}s")
        
        # Wait a moment for rendering
        time.sleep(1)
        
        # 3. Get Text from 'greeting_text'
        print("Finding greeting_text...")
        start_find_txt = time.perf_counter()
        greeting_element = self.flutter.find_by_key("greeting_text")
        find_txt_duration = time.perf_counter() - start_find_txt
        print(f"greeting_text element prepared in: {find_txt_duration:.4f}s")
        
        start_get_txt = time.perf_counter()
        text_val = greeting_element.text
        get_txt_duration = time.perf_counter() - start_get_txt
        
        print(f"Text retreived in: {get_txt_duration:.4f}s")
        print(f"Retrieved Greeting Text: '{text_val}'")
        
        # Summary
        print("\n--- Summary (u2_flutter) ---")
        print(f"Find Element:       {find_duration:.4f}s")
        print(f"Click Element:      {tap_duration:.4f}s")
        print(f"Find Text Element:  {find_txt_duration:.4f}s")
        print(f"Get Text Content:   {get_txt_duration:.4f}s")
        print(f"Total Action Round: {find_duration + tap_duration + find_txt_duration + get_txt_duration:.4f}s")

if __name__ == "__main__":
    bench = U2FlutterBenchmark()
    bench.run_benchmark()
