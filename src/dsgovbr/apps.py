from tabnanny import verbose
from django.apps import AppConfig


class DSGovBRConfig(AppConfig):
    name: str = "DSGovBR"
    verbose_name: str = "Outono de 2023"
    icon: str = "fa fa-edit"
    is_painel_theme: bool = True
