from django.urls import path 
from . import views

urlpatterns = [
    
    path('about/', views.about, name='about'),
    path('scrap/', views.scrapNews, name='scrap'),
    path('speech/', views.speechSynthesis, name='speech'),
    path('getblob/<str:newsId>/', views.getBlobData, name='getblob')
]