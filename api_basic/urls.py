
from django.contrib import admin
from django.urls import path,include
from .views import ArticleDetailView,ArticleView, GenericAPIViews
from rest_framework import routers


urlpatterns = [

    path('', ArticleView.as_view()),
    path('data_list_detail/<int:pk>/', ArticleDetailView.as_view()),
    path('generic/data_list/<int:id>/',  GenericAPIViews.as_view()),
   
]
