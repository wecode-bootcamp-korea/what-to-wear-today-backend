from django.urls import path
from . import views
from .views import UserView
from .views import LoginView
from .views import InfoView

urlpatterns = [
    path('', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('info/', InfoView.as_view())
]

