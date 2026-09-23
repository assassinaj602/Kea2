"""
Flutter Gallery Test Properties for Kea2
Tests various Flutter widgets in the official Gallery app
"""
import unittest
import logging

logger = logging.getLogger(__name__)

# Try to import u2_flutter, skip tests if not available
try:
    from u2_flutter import with_flutter
    HAS_U2_FLUTTER = True
except ImportError:
    HAS_U2_FLUTTER = False
    with_flutter = lambda func: func

from kea2 import precondition, prob

@unittest.skipIf(not HAS_U2_FLUTTER, "u2_flutter not installed")
class TestHybridApp(unittest.TestCase):
    """Test properties for Hybrid App (Phase 2: Native precondition -> Native action -> Flutter action)"""

    @with_flutter
    @prob(1.0)
    @precondition(lambda self: self.d(text="OPEN FLUTTER").exists)
    def test_native_to_flutter_flow(self):
        """
        Phase 2 demo: native precondition detects a real native control,
        clicks it, which navigates into the Flutter screen, then a Flutter
        action executes on that screen.
        """
        btn = self.d(text="OPEN FLUTTER")
        if btn.exists:
            btn.click()
            import time
            time.sleep(2.0)
        exists = self.flutter.find_by_key("HomeListView").exists
        logger.info(f"[RESULT] HomeListView exists = {exists}")
        assert exists, "Flutter screen did not load after native click"
        logger.info("[RESULT] Phase 2 flow completed successfully")
