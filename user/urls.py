from django.urls import path
from . import views
from .views import UserInfo

urlpatterns = [
    path('', UserInfo.as_view()),
]

