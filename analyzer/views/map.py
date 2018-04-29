import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from analyzer.models.sensor import Sensor
from analyzer.models.data_item import DataItem
from abc import ABC, abstractmethod


@method_decorator(login_required, name='dispatch')
class MapView(ABC, View):
    def get_marker_data(self, request):
        host = request.get_host()

        url_base = ('https://' if request.is_secure() else 'http://') + host + '/sensor?id='

        sensors = Sensor.objects.filter(user__username=request.user)

        data = list()

        for sensor in sensors:
            last_data_item = DataItem.objects.filter(sensor=sensor).latest('timestamp')
            sensor_item = dict(
                lat=float(last_data_item.latitude),
                lng=float(last_data_item.longitude),
                val=last_data_item.data,
                desc=f'<b>{sensor.title}</b><br>'
                     f'{str(sensor.type.title)}<br>'
                     f'{sensor.unit}<br>'
                     f'{str(last_data_item.data)}<br>'
                     f'<a target="_blank" href="{url_base}{str(sensor.id)}">See Full Data</a>'
            )
            data.append(sensor_item)

        return data

    @abstractmethod
    def get(self, request):
        pass


class PointMapView(MapView):
    template = 'pointmap.html'

    def get(self, request):
        marker_data = self.get_marker_data(request)
        data = json.dumps(marker_data)
        return render(request, self.template,
                      {'data': data,
                       'username': request.user.first_name + ' ' + request.user.last_name,
                       'email': request.user.email})


class HeatMapView(MapView):
    template = 'heatmap.html'

    def get(self, request):
        marker_data = self.get_marker_data(request)
        data = json.dumps(marker_data)
        return render(request, self.template,
                      {'data': data,
                       'username': request.user.first_name + ' ' + request.user.last_name,
                       'email': request.user.email})


class APIMapView(MapView):
    def get(self, request):
        marker_data = self.get_marker_data(request)
        return JsonResponse(marker_data, safe=False)
