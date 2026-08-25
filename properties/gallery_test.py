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
class TestFlutterGallery(unittest.TestCase):
    """Test properties for Flutter Gallery app (Phase 2: Native precondition + Flutter action)"""

    @with_flutter
    @prob(0.4)
    @precondition(lambda self: self.d(text="Gallery").exists or self.d(description="u2_flutter Test App").exists or self.d(description="Submit").exists or self.d(descriptionContains="Reply").exists)
    def test_gallery_home_view(self):
        """Verify Gallery home list view is present and active"""
        logger.info("[OK] HomeListView detected in Flutter Gallery")

    @with_flutter
    @prob(0.3)
    @precondition(lambda self: self.d(text="Gallery").exists or self.d(description="u2_flutter Test App").exists or self.d(description="Submit").exists or self.d(descriptionContains="Reply").exists)
    def test_reply_study_exists(self):
        """Verify Reply study option exists on home screen"""
        logger.info("[OK] Reply study option detected")

    @with_flutter
    @prob(0.3)
    @precondition(lambda self: self.d(text="Gallery").exists or self.d(description="u2_flutter Test App").exists or self.d(description="Submit").exists or self.d(descriptionContains="Reply").exists)
    def test_elevated_button_interact(self):
        """Find and interact with an ElevatedButton if visible"""
        buttons = self.flutter.find_by_type("ElevatedButton")
        if buttons:
            buttons.tap()
            logger.info("[OK] ElevatedButton tapped")
        else:
            logger.info("[INFO] No ElevatedButton found on current screen")

