# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('parse/', views.parse_news, name='parse_page'),  # Изменили на parse_news
]