from . import views
from .views import PingView

from django.urls import include, path

urlpatterns = [
    path('user', include('user.urls')),
    path('weather', include('weather.urls')),
    path('clothes', include('clothes.urls')),
    path('ping', PingView.as_view())
]
