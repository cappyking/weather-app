from __future__ import absolute_import,unicode_literals
from .celery import Celery as celery_app

__app__ = ('celery_app',)