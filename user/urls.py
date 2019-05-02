from django.urls import path

from . import views
from .views import UserView
from .views import AuthView
from .views import CredentialView

urlpatterns = [
    path('', UserView.as_view()),
    path('/auth', AuthView.as_view()),
    path('/credential', CredentialView.as_view())
]

