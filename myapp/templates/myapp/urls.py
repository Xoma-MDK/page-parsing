from django.urls import path
from . import views

urlpatterns = [
    path('parse/', views.parse_lenta, name='parse_page'),
    path('', views.article_list, name='article_list'),
]