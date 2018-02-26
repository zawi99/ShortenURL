from django.conf import settings
from django.db import models

from django.urls import reverse

from .utils import create_shortcode
from .validators import validate_url

BASE_URL = getattr(settings, 'DEFAULT_REDIRECT_URL', 'localhost:8000')
SHORTCODE_MAX = getattr(settings, 'SHORTCODE_MAX', 15)


class ShrtnURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(ShrtnURLManager, self)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = ShrtnURL.objects.filter(pk__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for obj in qs:
            obj.shortcode = create_shortcode(obj)
            obj.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)


class ShrtnURL(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = ShrtnURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        if not 'http' in self.url:
            self.url = 'http://' + self.url
        super(ShrtnURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse('scode', kwargs={'shortcode': self.shortcode})
        return BASE_URL + url_path
