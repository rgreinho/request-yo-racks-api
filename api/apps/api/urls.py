"""Define the API URLs."""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.apps.api import views

urlpatterns = [
    url(r'health$', views.Health.as_view()),
    url(r'places/(?P<latlong>[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?))$',
        views.PlaceList.as_view()),
    url(r'place/(?P<pid>.*)/$', views.PlaceDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
