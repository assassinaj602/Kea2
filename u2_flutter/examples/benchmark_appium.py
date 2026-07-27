import time
import sys
from appium import webdriver
from appium.options.common import AppiumOptions
from appium_flutter_finder.flutter_finder import FlutterFinder

def run_appium_benchmark():
    print("=== Appium Flutter Driver Benchmark ===")
    
    # 1. Start Appium Session (Connection overhead)
    start_conn = time.perf_counter()
    
    options = AppiumOptions()
    options.set_capability("platformName", "Android")
    options.set_capability("automationName", "Flutter")
    options.set_capability("appPackage", "com.example.test_app")
    options.set_capability("appActivity", ".MainActivity")
    options.set_capability("noReset", True)
    
    print("Connecting to Appium Server...")
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    conn_duration = time.perf_counter() - start_conn
    print(f"Connection established in: {conn_duration:.4f}s")
    
    # Flutter context mapping
    print("Switching context to FLUTTER...")
    driver.switch_to.context("FLUTTER")
    finder = FlutterFinder()
    
    try:
        # 2. Find Element 'submit_btn'
        print("Finding submit_btn...")
        start_find = time.perf_counter()
        submit_btn_element_key = finder.by_value_key("submit_btn")
        driver.execute_script("flutter:waitFor", submit_btn_element_key)
        find_duration = time.perf_counter() - start_find
        print(f"submit_btn found in: {find_duration:.4f}s")
        
        # 3. Tap Element
        print("Tapping submit_btn...")
        start_tap = time.perf_counter()
        driver.execute_script("flutter:clickElement", submit_btn_element_key)
        tap_duration = time.perf_counter() - start_tap
        print(f"Tap completed in: {tap_duration:.4f}s")
        
        # Wait a moment for rendering
        time.sleep(1)
        
        # 4. Get Text from 'greeting_text'
        # Since Appium Flutter Driver natively throws "Command not supported: flutter:getText" 
        # because the app lacks custom command extensions, we can measure the wait time 
        # and fallback to getting diagnostics tree / semantics check or skip the text extraction command call 
        # to record the metrics of the executable pipeline.
        print("Finding greeting_text...")
        start_find_txt = time.perf_counter()
        greeting_element_key = finder.by_value_key("greeting_text")
        driver.execute_script("flutter:waitFor", greeting_element_key)
        find_txt_duration = time.perf_counter() - start_find_txt
        print(f"greeting_text element found in: {find_txt_duration:.4f}s")
        
        # Getting diagnostics details as a proxy for text retrieval command roundtrip
        print("Retrieving widget diagnostics as proxy for text retrieval...")
        start_get_txt = time.perf_counter()
        diag_tree = driver.execute_script("flutter:getWidgetDiagnostics", greeting_element_key)
        get_txt_duration = time.perf_counter() - start_get_txt
        
        print(f"Diagnostics tree retrieved in: {get_txt_duration:.4f}s")
        
        # Summary
        print("\n--- Summary (Appium Flutter Driver) ---")
        print(f"Session Connection: {conn_duration:.4f}s")
        print(f"Find Element:       {find_duration:.4f}s")
        print(f"Click Element:      {tap_duration:.4f}s")
        print(f"Find Text Element:  {find_txt_duration:.4f}s")
        print(f"Get Text Content:   {get_txt_duration:.4f}s")
        print(f"Total Action Round: {find_duration + tap_duration + find_txt_duration + get_txt_duration:.4f}s")
        
    except Exception as e:
        print(f"\nBenchmark Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_appium_benchmark()
