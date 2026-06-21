from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<slug:slug>/', views.article_detail, name='article_detail'),
    path('news/<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<slug:slug>/', views.review_detail, name='review_detail'),
    path('refresh-news-stream/', views.force_api_refresh, name='api_refresh'),
    path('about-developer/', views.about_and_support, name='about_support'),
]