from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('user', views.user, name='user'),
    path('question_1', views.question_1, name='question_1'),
    path('question_2', views.question_2, name='question_2'),
    path('question_3', views.question_3, name='question_3'),
    path('question_4', views.question_4, name='question_4'),
    path('question_5', views.question_5, name='question_5'),
]
