from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class DbLabConfig(AppConfig):
    name = 'db_lab'


class MyAppConfig(ModuleMixin, AppConfig):
    name = 'myapp'
    icon = '<i class="material-icons">flight_takeoff</i>'
