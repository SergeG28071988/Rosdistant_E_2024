from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  
    path('human_lis', views.human_list, name='human_list'), 
    path('create', views.create, name='create'),
]