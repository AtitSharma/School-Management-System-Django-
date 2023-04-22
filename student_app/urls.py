
from django.urls import path
from student_app.views import (home,Login,
                               register,student_home,
                               admin_home,student_login
                               ,manage,add_student,
                               add_teacher,
                               add_course,add_subject,add_semister
                               ,EditCourse,create_post,EditPost,DeletePost,
                               EditStudent,EditSemister,
                               DeleteStudent,EditTeacher,DeleteTeacher
                               ,EditSubject,DeleteSemister,DeleteCourse,DeleteSubject
                               )

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
    path("add-teacher/",add_teacher,name="add_teacher"),
    path("add-course/",add_course,name="add_course"),
    path("add-subject/",add_subject,name="add_subject"),
    path("add-semister/",add_semister,name="add_semister"),
    path("edit-course/<int:pk>",EditCourse.as_view(),name="edit_course"),
    path("edit-student/<int:pk>",EditStudent.as_view(),name="edit_student"),
    path("edit-subject/<int:pk>",EditSubject.as_view(),name="edit_subject"),
    path("edit-semister/<int:pk>",EditSemister.as_view(),name="edit_semister"),
    path("edit-teacher/<int:pk>",EditTeacher.as_view(),name="edit_teacher"),
    path("delete-student/<int:pk>",DeleteStudent.as_view(),name="delete_student"),
    path("delete-semister/<int:pk>",DeleteSemister.as_view(),name="delete_semister"),
    path("delete-subject/<int:pk>",DeleteSubject.as_view(),name="delete_subject"),
    path("delete-teacher/<int:pk>",DeleteTeacher.as_view(),name="delete_teacher"),
    path("delete-course/<int:pk>",DeleteCourse.as_view(),name="delete_course"),
    path("create-post/",create_post,name="create_post"),
    path("edit-post/<int:pk>",EditPost.as_view(),name="edit_post"),
    path("delete-post/<int:pk>",DeletePost.as_view(),name="delete_post"),



]