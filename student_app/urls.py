
from django.urls import path
from student_app.views import (home,Login,
                               register,student_home,
                               admin_home,student_login
                               ,manage,add_student)

app_name="student"

urlpatterns = [
    path("",home,name="home"),
    path("login/",Login.as_view(),name="login"),
    path("register/",register,name="register"),
    path("student-home/",student_home,name="student_home"),
    path("admin-home/",admin_home,name="admin_home"),
    path("student-login/",student_login,name="student_login"),
    path("manage/<str:title>/",manage,name="manage"),
    path("add-student/",add_student,name="add_stundent"),

]