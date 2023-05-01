from rest_framework import serializers

from student_app.models import Teacher,Student,Semister,Subject,User,Course,Post




class TeacherSerializer(serializers.ModelSerializer):
    class Meta:

        model=Teacher
        fields=["name","description","user","due_salary","subject","id"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=["name","description","user","id"]


class SemisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Semister
        fields=["name","description","teacher","student","subject","id"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=["name","description","marks","id"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=["title","description","user","id"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","id"]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=["teacher","student","semister","id"]
