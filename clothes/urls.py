from django.urls import path   

from . import views
from .views import HeartView    
        
urlpatterns = [
    path('/heart', HeartView.as_view()),
]   

