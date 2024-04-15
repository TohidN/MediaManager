from django.conf.urls import include
from django.urls import path, re_path
from . import views

app_name = "media"
urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('media/<slug:slug>/', views.media_detail, name='media_detail'),
    path('<int:media_id>/rate/', views.add_user_rating, name='add_user_rating'),
    path('media/<int:media_id>/reviews/', views.media_reviews, name='media_reviews'),
    path('person/<int:pk>/', views.person_detail, name='person_detail'),
]