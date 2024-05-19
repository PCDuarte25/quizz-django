from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user', views.user, name='user'),
    path('question_1/<int:person_id>', views.question_1, name='question_1'),
    path('question_2/<int:person_id>', views.question_2, name='question_2'),
    path('question_3/<int:person_id>', views.question_3, name='question_3'),
    path('question_4/<int:person_id>', views.question_4, name='question_4'),
    path('question_5/<int:person_id>', views.question_5, name='question_5'),
]
