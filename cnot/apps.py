"""
cnot Django application initialization.
"""

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class CnotEdxConfig(AppConfig):
    """
    Configuration for the cnot Django application.
    """

    name = 'cnot'

    def ready(self) -> None:
        pass


class CNOTAdminConfig(AdminConfig):
    # default_site = 'cnot.admin.CNOTAdminSite'
    name = 'cnot.admin.CNOTAdminSite'
    label = 'cnot_admin'
