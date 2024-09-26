from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import GraphModel  # Assuming the model is in models.py


class GraphDisplayView(ListView):
    model = GraphModel
    template_name = 'graph_view.html'
    context_object_name = 'graphs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional_info'] = 'This is some extra information'
        return context

    def get(self, request, *args, **kwargs):
        """ Handles GET request. """
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


@csrf_exempt
def api_data_view(request):
    """ API endpoint for sending graph data in JSON format. """
    if request.method == 'GET':
        graph_data = {}  # Assuming you populate this with the actual graph data
        return JsonResponse(graph_data, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)
