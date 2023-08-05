from django.conf import settings

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class EventsApp(CMSApp):
    """
    App hook for Events app
    """

    app_name = "giant_events"
    name = "Giant Events"

    def get_urls(self, page=None, language=None, **kwargs):
        """
        Return the path to the apps urls module
        """

        return ["events.urls"]


if settings.REGISTER_EVENTS_APP:
    apphook_pool.register(NewsApp)
