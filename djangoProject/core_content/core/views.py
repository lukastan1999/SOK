from django.apps.registry import apps
from django.shortcuts import render, redirect
from core.services.graphService import GraphService


def index(request):
    config = apps.get_app_config('core').config
    for k, v in config.items():
        print(k, v)
    return render(request, "index.html", {"title": "Index",
                                          "config": config})


def load_data_plugin(request):
    data_plugins = apps.get_app_config('core').config['data_plugins']

    plugin_id = request.POST["dataPluginSelect"]
    source = request.POST["izvorSelect"]
    file_name = request.POST["inputFile"]
    url = request.POST["urlInput"]

    for p in data_plugins:
        if p.identifier() == plugin_id:
            if source == "fajl":
                apps.get_app_config('core').config['graph'] = p.load_data(file_name)
            else:
                apps.get_app_config('core').config['graph'] = p.load_data(url)
            apps.get_app_config('core').config['savedGraph'] = apps.get_app_config('core').config['graph']

    return redirect('index')


def load_view_bird(request):
    config = apps.get_app_config('core').config
    graph = config["graph"]
    if graph is None:
        return redirect('index')

    vertices = graph.vertices()
    linksS = graph.edges()
    links = []
    for link in linksS:
        ret = []
        c1, c2 = link.endpoints()
        ret.append(c1.Id)
        ret.append(c2.Id)
        links.append(ret)

    return render(request, "bird.html", {"title": "BirdView", "config": config, "vertices": vertices, "links": links})


def load_view_plugin(request):
    view_plugins = apps.get_app_config('core').config['view_plugins']
    graph = apps.get_app_config('core').config['graph']
    plugin_id = request.POST["viewPluginSelect"]
    htmlCode = ''
    for p in view_plugins:
        if p.identifier() == plugin_id:
            htmlCode = p.load_view(graph)
    apps.get_app_config('core').config['currentViewPluginHtml'] = htmlCode
    return redirect('index')


def filter_graph(request):
    atr = request.POST["filterAtribut"]
    operator = request.POST["filterOperator"]
    value = request.POST["filterVrednost"]

    graph = apps.get_app_config('core').config['graph']
    apps.get_app_config('core').config['graph'] = GraphService.filter(graph, atr, operator, value)

    return redirect('index')


def search_graph(request):
    query = request.POST["searchPolje"]

    graph = apps.get_app_config('core').config['graph']
    apps.get_app_config('core').config['graph'] = GraphService.search(graph, query=query)

    return redirect('index')


def reset_to_default_graph(request):
    apps.get_app_config('core').config['graph'] = apps.get_app_config('core').config['savedGraph']
    return redirect('index')
