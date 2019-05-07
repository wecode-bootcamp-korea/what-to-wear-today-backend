from django.urls import path   

from . import views
from .views import HeartView    
from .views import Top10View

urlpatterns = [
    path('/heart', HeartView.as_view()),
    path('/top10', Top10View.as_view())
]   

