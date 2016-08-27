from django.conf.urls import url

from .views import (
    RadioPlayAPIView, PlayerCommandAPIView, RadioListAPIView,
    PlayerStatusAPIView, MP3PlaylistAPIView
)

urlpatterns = [
    url(r'^player/status/$', PlayerStatusAPIView.as_view(), name='status'),
    url(r'^player/command/$', PlayerCommandAPIView.as_view(), name='command'),
    url(r'^player/playlist/$', MP3PlaylistAPIView.as_view(), name='playlist'),

    url(r'^radios/$', RadioListAPIView.as_view(), name='radio_list'),
    url(r'^radios/(?P<pk>[\w-]+)/$', RadioPlayAPIView.as_view(), name='play'),
]
