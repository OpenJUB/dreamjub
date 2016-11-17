from django.db import models
from oauth2_provider import models as oauth_models
from django import conf

# Create your models here.


class WidgetVersion(models.Model):
    type = models.ForeignKey(WidgetType, models.PROTECT,
                             related_name='versions',
                             related_query_name='version')

    # Filename and DOM element name of this widget version
    entry_file = models.CharField(max_length=256)
    entry_element = models.CharField(max_length=256)

    # Hash of the package, and the manifest content
    hash = models.CharField(max_length=64)
    manifest = models.TextField()

    # Creation and access date
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Governs the availability of this version to end users
    active = models.BooleanField(default=False)


class WidgetType(models.Model):
    """A type of widget, for example a clock or simple notepad"""
    owner = models.ForeignKey(oauth_models.Application)


class Widget(models.Model):
    """An instance of a widget, created when added to homepage by user"""
    uuid = models.UUIDField()
    owner = models.ForeignKey(conf.settings.AUTH_USER_MODEL)

    # Type of this widget
    type = models.ForeignKey(WidgetType, on_delete=models.CASCADE,
                             related_name='instances',
                             related_query_name='instance')

    # Display settings
    order = models.PositiveSmallIntegerField(default=0)
    settings = models.TextField()

    # Date tracking
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)