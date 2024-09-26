from django.apps import apps
from django.shortcuts import render

# Create your views here.
def index(request):
    config = apps.get_app_config('core').config
    for k, v in config.items():
        print(k, v)
    return render(request, "index.html", {"title": "Index",
                                          "config": config})