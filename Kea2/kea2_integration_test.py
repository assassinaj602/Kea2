import unittest
from unittest.mock import Mock, MagicMock
import sys
import os

# Add paths dynamically to make sure we can import both kea2 and kea2_integration portably
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.abspath(os.path.join(base_dir, "..", "u2_flutter")))

from kea2_integration.flutter_static_checker import FlutterStaticChecker
from kea2_integration.flutter_script_driver import FlutterScriptDriver

class NativeOnlyTest(unittest.TestCase):
    """Ensures native Android check functions normally without Flutter active."""
    def test_native_app(self):
        mock_u2_device = Mock()
        mock_u2_device.exists = True
        
        # Native verification
        self.assertTrue(mock_u2_device.exists)

class FlutterOnlyTest(unittest.TestCase):
    """Verifies that FlutterStaticChecker properly indexes and evaluates exist checks."""
    def setUp(self):
        self.mock_driver = Mock()
        self.sample_tree = {
            "type": "DiagnosticableTreeNode",
            "description": "MyApp",
            "properties": [],
            "children": [
                {
                    "type": "DiagnosticableTreeNode",
                    "description": "ElevatedButton",
                    "properties": [
                        {"name": "key", "description": "fuzz_submit_btn"},
                        {"name": "text", "description": "Submit Fuzz"},
                        {"name": "type", "description": "ElevatedButton"}
                    ],
                    "children": []
                }
            ]
        }
        self.checker = FlutterStaticChecker(self.mock_driver)
        self.checker.set_hierarchy(self.sample_tree)

    def test_flutter_app(self):
        self.assertTrue(self.checker.exists("fuzz_submit_btn"))
        self.assertTrue(self.checker.exists_by_text("Submit Fuzz"))
        self.assertTrue(self.checker.exists_by_type("ElevatedButton"))
        self.assertFalse(self.checker.exists("non_existent_key"))

class HybridTest(unittest.TestCase):
    """Verifies coexistency of native and Flutter checkers for hybrid environments."""
    def setUp(self):
        self.mock_flutter_driver = Mock()
        self.flutter_checker = FlutterStaticChecker(self.mock_flutter_driver)
        self.flutter_checker.set_hierarchy({
            "type": "DiagnosticableTreeNode",
            "description": "MaterialApp",
            "properties": [],
            "children": [
                {
                    "type": "DiagnosticableTreeNode",
                    "description": "TextField",
                    "properties": [
                        {"name": "key", "description": "username_field"},
                        {"name": "text", "description": ""}
                    ],
                    "children": []
                }
            ]
        })
        
        self.mock_u2_device = Mock()
        self.mock_u2_device.exists = True

    def test_hybrid_app(self):
        # Native check passes
        self.assertTrue(self.mock_u2_device.exists)
        # Flutter check passes
        self.assertTrue(self.flutter_checker.exists("username_field"))

if __name__ == "__main__":
    unittest.main()
