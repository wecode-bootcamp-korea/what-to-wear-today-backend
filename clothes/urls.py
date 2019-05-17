from django.urls import path   

from . import views
from .views import HeartView, HeartCheck    
from .views import TopImageView

urlpatterns = [
    path('/heart', HeartView.as_view()),
    path('/top', TopImageView.as_view()),
    path('/heart/check', HeartCheck.as_view())
]   

