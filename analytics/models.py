from django.db import models

from shortener.models import ShrtnURL


class ClickEventManager(models.Manager):
    def create_event(self, shrtnInstance):
        if isinstance(shrtnInstance, ShrtnURL):
            obj, created = self.get_or_create(shrtn_url=shrtnInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    shrtn_url = models.OneToOneField(ShrtnURL)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = ClickEventManager()

    def __str__(self):
        return '{i} -> {url}'.format(i=self.count, url=self.shrtn_url)