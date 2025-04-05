from django.urls import path
from .import views

urlpatterns = [
    
    path('student/register/',views.RegisterStudent.as_view(),name="register_student"),
    path('faculty/register/',views.RegisterFaculty.as_view(),name="register_view"),
    path('users/login/',views.LoginView.as_view(),name="login_users"),
    path('add/course/',views.AddCourse.as_view(),name="add_course"),
    path('register/course/',views.RegisterCourse.as_view(),name="register_course"),    
    
]
