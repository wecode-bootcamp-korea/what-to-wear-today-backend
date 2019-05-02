from django.urls import include, path

urlpatterns = [
    path('user', include('user.urls'))
    path('weather', include('weather.urls')),
]
