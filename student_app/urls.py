
from django.urls import path,include
from student_app.views import (home,send_mails_to_all,search,
                               register,student_home,
                               admin_home,view_admission,view_complaints
                               ,add_student,Login,
                               add_teacher,contact,contact_for_admission,contact_for_message,
                               add_course,add_subject,add_semister,user_logout
                               ,EditCourse,create_post,EditPost,delete_post,
                               EditStudent,EditSemister,ProfileUpdateStudent,
                               delete_student,EditTeacher,delete_teacher
                               ,EditSubject,delete_semister,delete_subject,delete_course
                               )




app_name="student"

urlpatterns = [
    path("",home,name="home"),
    # path("login/",Login.as_view(),name="login"),
    
    path("contact/",contact,name="contact"),
    path("contact-admission/",contact_for_admission,name="contact_admission"),
    path("contact-complaint/",contact_for_message,name="contact_message"),
    path("logout",user_logout,name="logout"),
    path("register/",register,name="register"),
    path("student-home/",student_home,name="student_home"),
    path("admin-home/",admin_home,name="admin_home"),
    path("student-login/",Login.as_view(),name="student_login"),
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
    path("delete-student/<int:pk>",delete_student,name="delete_student"),
    path("delete-semister/<int:pk>",delete_semister,name="delete_semister"),
    path("delete-subject/<int:pk>",delete_subject,name="delete_subject"),
    path("delete-teacher/<int:pk>",delete_teacher,name="delete_teacher"),
    path("delete-course/<int:pk>",delete_course,name="delete_course"),
    path("create-post/",create_post,name="create_post"),
    path("edit-post/<int:pk>",EditPost.as_view(),name="edit_post"),
    path("delete-post/<int:pk>",delete_post,name="delete_post"),
    path("edit-profile/<int:pk>",ProfileUpdateStudent.as_view(),name="profile_update"),
    path("view-admission/",view_admission,name="view_admission"),
    path("view-complaints/",view_complaints,name="view_complaints"),
    path("search/",search,name="search")




]