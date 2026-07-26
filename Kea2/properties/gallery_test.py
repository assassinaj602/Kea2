"""
Flutter Gallery Test Properties for Kea2
Tests various Flutter widgets in the official Gallery app
"""
import unittest
import logging
from kea2 import precondition, prob
from u2_flutter import with_flutter

logger = logging.getLogger(__name__)

class TestFlutterGallery(unittest.TestCase):
    """Test properties for Flutter Gallery app"""
    
    @with_flutter
    @prob(0.4)
    @precondition(lambda self: self.flutter.find_by_key("HomeListView").exists)
    def test_gallery_home_view(self):
        """Verify Gallery home list view is present and active"""
        logger.info("✅ HomeListView detected in Flutter Gallery")

    @with_flutter
    @prob(0.3)
    @precondition(lambda self: self.flutter.find_by_text("Reply").exists)
    def test_reply_study_exists(self):
        """Verify Reply study option exists on home screen"""
        logger.info("✅ Reply study option detected")

    @with_flutter
    @prob(0.3)
    @precondition(lambda self: self.flutter.find_by_type("ElevatedButton").exists)
    def test_elevated_button_interact(self):
        """Find and interact with an ElevatedButton if visible"""
        buttons = self.flutter.find_by_type("ElevatedButton")
        if buttons:
            buttons.tap()
            logger.info("✅ ElevatedButton tapped")
        else:
            logger.info("ℹ️ No ElevatedButton found on current screen")
