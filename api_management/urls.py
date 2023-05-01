from django.urls import path,include
from rest_framework import routers 

router=routers.SimpleRouter()

# router.register("tasks",TaskViewSet,basename="task")
# router.register("category",CategoryViewSet,basename="category")
from api_management.views import PostViewSet,UserViewSet,CourseViewSet,SemisterViewSet,StudentViewSet,SubjectViewSet,serializer1,TeacherViewSet

router.register("posts",PostViewSet,basename="post")
router.register("users",UserViewSet,basename="user")
router.register("courses",CourseViewSet,basename="course")
router.register("semisters",SemisterViewSet,basename="semister")
router.register("students",StudentViewSet,basename="student")
router.register("subjects",SubjectViewSet,basename="subject")
router.register("teachers",TeacherViewSet,basename="teacher")

app_name="api"
urlpatterns=[
    path("",include(router.urls)),
    path("serializer/",serializer1,name="serializer")


]

