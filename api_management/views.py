from django.shortcuts import render
from api_management.serializers import (TeacherSerializer,SemisterSerializer,
                                        StudentSerializer,SubjectSerializer,
                                        CourseSerializer,UserSerializer,PostSerializer)
from student_app.models import (User
                                ,Student,Teacher
                                ,Semister,Subject
                                ,Course,Post)
from rest_framework.viewsets import ModelViewSet
from student_app.forms import StudentCreationForm



class TeacherViewSet(ModelViewSet):
    serializer_class=TeacherSerializer
    queryset=Teacher.objects.all()


class SemisterViewSet(ModelViewSet):
    serializer_class=SemisterSerializer
    queryset=Semister.objects.all()

class StudentViewSet(ModelViewSet):
    serializer_class=StudentSerializer
    queryset=Student.objects.all()

class UserViewSet(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()


class PostViewSet(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all()

class SubjectViewSet(ModelViewSet):
    serializer_class=SubjectSerializer
    queryset=Subject.objects.all()

class CourseViewSet(ModelViewSet):
    serializer_class=CourseSerializer
    queryset=Course.objects.all()


def serializer1(request):
    form=StudentCreationForm()
    context={
        "form":form
    }
    return render(request,"student_app/serializer.html",context)
    

