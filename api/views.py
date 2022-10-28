from django.shortcuts import render
from django.views.generic import View
from api.serializers import *
from api.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer



# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@api_view(('GET',))
def monitors(self, *args, **kwargs):
        all_monitors = Monitor.objects.all()
        print(all_monitors)
        monitors_data = MonitorData(all_monitors, many=True)
        print(monitors_data.data)
        return Response(monitors_data.data, status=200)
