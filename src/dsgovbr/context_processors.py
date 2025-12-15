from django.conf import settings
from django.utils.translation import gettext as _
from django.http import HttpRequest


def layout_settings(request: HttpRequest) -> dict:
    return {
        "app_label": getattr(settings, "APP_LABEL", "APP_LABEL"),
        "app_version": getattr(settings, "APP_VERSION", "APP_VERSION"),
        "app_last_startup": getattr(settings, "APP_LAST_STARTUP", "APP_LAST_STARTUP"),
        "hostname": getattr(settings, "HOSTNAME", "HOSTNAME"),
        "user_avatar": "https://cdn-icons-png.freepik.com/512/6596/6596121.png",
        "have_header_menu_trigger": True,
        "fast_access_links": getattr(
            settings,
            "APP_FAST_ACCESS_LINKS", 
            [
                {'url': '/', 'label': 'Home'}
            ]
        ),
        "feature_links": getattr(
            settings,
            "APP_FEATURE_LINKS", 
            [
                {'icon': 'fas fa-adjust', 'label': 'Funcionalidade 1'}
            ]
        ),
    }
