"""Define the API URLs."""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.apps.api import views

urlpatterns = [
    url(r'^places/$', views.PlaceList.as_view()),
    url(r'^place/(?P<pid>[0-9a-zA-Z\-]+)/$', views.PlaceDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
