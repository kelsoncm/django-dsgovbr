from django.conf import settings
from django.utils.translation import gettext as _
from django.http import HttpRequest


def layout_settings(request: HttpRequest) -> dict:
    return {
        "project_company": getattr(settings, "PROJECT_COMPANY", "PROJECT_COMPANY"),
        "project_title": getattr(settings, "PROJECT_TITLE", "PROJECT_TITLE"),
        "project_subtitle": getattr(settings, "PROJECT_SUBTITLE", "PROJECT_SUBTITLE"),
        "project_version": getattr(settings, "PROJECT_VERSION", "PROJECT_VERSION"),
        "project_last_startup": getattr(settings, "PROJECT_LAST_STARTUP", "PROJECT_LAST_STARTUP"),
        "project_copyright": getattr(settings, "PROJECT_COPYRIGHT", "@2025 PROJECT_COPYRIGHT"),
        "project_license": getattr(settings, "PROJECT_LICENSE", "Licença MIT"),
        "project_license_url": getattr(settings, "PROJECT_LICENSE_URL", "https://opensource.org/license/mit"),

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
