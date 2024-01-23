from django.urls import path

from .webhook import webhook, set_webhook


urlpatterns = [
    path('webhook/', webhook),
    path('set-webhook/', set_webhook),
]
