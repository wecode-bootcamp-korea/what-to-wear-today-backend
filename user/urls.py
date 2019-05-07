from django.urls import path

from . import views
from .views import UserView
from .views import AuthView
from .views import CredentialView, UserSettingUpdateView, UserSettingView

urlpatterns = [
    path('', UserView.as_view()),
    path('/auth', AuthView.as_view()),
    path('/credential', CredentialView.as_view()),
    path('/update', UserSettingUpdateView.as_view()),
    path('/setting', UserSettingView.as_view())
]

