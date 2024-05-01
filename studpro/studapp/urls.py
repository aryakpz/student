from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home.as_view()),
    path('student-information', views.student_information, name='student_information'),
    path('student-mark/', views.student_mark, name='student_mark'),
    path('edit-student/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:pk>/', views.delete_student, name='delete_student'),
]
