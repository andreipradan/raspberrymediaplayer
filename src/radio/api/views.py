import logging
from collections import OrderedDict

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .utils import send_command
from ..entities.models import Station

logger = logging.getLogger(__name__)


class PlayerStatusAPIView(RetrieveAPIView):
    def get(self, request, **kwargs):
        response = send_command("mpc").split('\n')[:-1]
        try:
            response[-1] = response[-1].split(' repeat')[0]
        except IndexError:
            pass
        return Response(" :: ".join(response))


class PlayerCommandAPIView(RetrieveAPIView):
    def get(self, request, **kwargs):
        if len(request.query_params) > 1:
            first = request.query_params.get('first')
            second = request.query_params.get('second')
            query_params = [x for x in (first, second) if x]
        else:
            query_params = list(request.query_params)
        response = send_command('mpc', *query_params).split('\n')[:-1]
        try:
            response[-1] = response[-1].split(' repeat')[0]
        except IndexError:
            pass
        logger.info('Sent: mpc {}. Response: {}'.format(query_params, response))
        return Response(" :: ".join(response))


class RadioListAPIView(ListAPIView):
    def get(self, request, **kwargs):
        station_list = Station.objects.all()
        response = OrderedDict()
        response['Number of stations'] = len(station_list)
        response['stations'] = OrderedDict()
        for station in station_list:
            response['stations'][station.name] = station.url
        return Response(response)


class RadioPlayAPIView(RetrieveAPIView):
    @staticmethod
    def play_single_file(file):
        send_command('mpc', 'clear')
        send_command('mpc', 'add', file)
        send_command('mpc', 'add', file)
        send_command('mpc', 'play')

    def get(self, request, **kwargs):
        station = get_object_or_404(Station, pk=kwargs.get('pk'))
        self.play_single_file(station.url)
        return Response('Playing {}'.format(station.name))


class MP3PlaylistAPIView(RetrieveAPIView):
    def get(self, request, **kwargs):
        send_command('mpc', 'clear')
        all_music = send_command('mpc', 'listall').split('\n')[:-1]
        for song in all_music:
            send_command('mpc', 'add', song)
        return Response(send_command('mpc', 'playlist').split('\n'))
