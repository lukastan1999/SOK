from django.apps import AppConfig
from core.tests import create_small_tree

import pkg_resources

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    config = {'data_plugins': [],
              'view_plugins': [],
              'currentViewPluginHtml': None,
              'graph': None,
              'savedGraph': None
             }

    def ready(self):
        self.config['data_plugins'] = load_plugins("data_load")
        self.config['view_plugins'] = load_plugins("view_load")


def load_plugins(oznaka):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins

