from django.urls import path
from . import views
from .views import UserView
from .views import LoginView
from .views import InfoView
from .views import ChangeView

urlpatterns = [
    path('signup', UserView.as_view()),
    path('login', LoginView.as_view()),
    path('info', InfoView.as_view()),
    path('change', ChangeView.as_view())
]

