from django.urls import path
from core import views, apps

urlpatterns = [
    path('', views.index, name="index"),
    path('load/data/plugin', views.load_data_plugin, name="load_data_plugin"),
    path('load/view/plugin', views.load_view_plugin, name="load_view_plugin")
    ]