from django.urls import path
from core import views, apps

urlpatterns = [
    path('', views.index, name="index"),
    path('load/data/plugin', views.load_data_plugin, name="load_data_plugin"),
    path('load/view/plugin', views.load_view_plugin, name="load_view_plugin"),
    path('load/view/bird', views.load_view_bird, name="load_view_bird"),
    path('filter/graph', views.filter_graph, name="filter_graph"),
    path('reset/to/default/graph', views.reset_to_default_graph, name="reset_to_default_graph"),
    path('search/graph', views.search_graph, name="search_graph")

]