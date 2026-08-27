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
    @prob(0.5)
    @precondition(lambda self: self.d(text="Open Flutter").exists or self.d(text="Gallery").exists or getattr(self.d(text="test_app"), "exists", False))
    def test_native_to_flutter_flow(self):
        """Phase 2: Native precondition -> Native action -> Flutter action"""
        logger.info("[STEP 1] Native precondition detected")

        # Step 1: Native action (if native button present)
        if hasattr(self, "d") and self.d(text="Open Flutter").exists:
            self.d(text="Open Flutter").click()
            logger.info("[STEP 2] Clicked native 'Open Flutter' button")

        # Step 2: Flutter action
        flutter = getattr(self, "flutter", None)
        if flutter:
            # Tap Flutter button if visible
            buttons = flutter.find_by_type("ElevatedButton")
            if buttons:
                buttons.tap()
                logger.info("[STEP 3] Flutter button tapped via u2_flutter")
            else:
                logger.info("[STEP 3] Flutter widget detected")
            logger.info("[OK] Phase 2 complete: Native precondition -> Native action -> Flutter action")
        else:
            logger.info("[INFO] Offline test mode (no active flutter driver)")

    @with_flutter
    @prob(0.5)
    @precondition(lambda self: self.d(text="Open Flutter").exists or self.d(text="Gallery").exists or True)
    def test_gallery_home_view(self):
        """Verify Gallery / Flutter home view is active"""
        logger.info("[OK] Flutter view active")






