from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('1/', views.solution1, name='solution1'),
    path('2/', views.solution2, name='solution2'),
    path('3/', views.solution3, name='solution3'),
    path('4/', views.solution4, name='solution4'),
    path('5/', views.solution5, name='solution5'),
]