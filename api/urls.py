from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from api.apps.api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Health.as_view()),
    url(r'^', include('api.apps.api.urls')),
]
