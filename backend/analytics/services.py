import logging
from django.conf import settings
import posthog

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.client = None
        if getattr(settings, 'POSTHOG_API_KEY', None):
            self.client = posthog.PostHog(
                settings.POSTHOG_API_KEY,
                host=getattr(settings, 'POSTHOG_HOST', 'https://app.posthog.com')
            )

    def track(self, user_id, event, properties=None):
        if not self.client:
            return
        
        # Privacy check: Check DNT or user consent status (simplified)
        # In real app, check user profile or request context
        
        try:
            self.client.capture(user_id, event, properties)
        except Exception as e:
            logger.error(f"PostHog tracking failed: {e}")

