from tabnanny import verbose
from django.apps import AppConfig


class DSGovBRConfig(AppConfig):
    name: str = "dsgovbr"
    verbose_name: str = "DSGovBR"
    icon: str = "fa fa-edit"
