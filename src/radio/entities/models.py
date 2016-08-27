from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=200)

    url = models.URLField(max_length=512, blank=False,
                          verbose_name="Playable URL of the radio stream")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
