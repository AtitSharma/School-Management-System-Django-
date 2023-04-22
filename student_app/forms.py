from django import forms
from django.contrib.auth.forms import UserCreationForm
from student_app.models import (User
                                ,Student,Teacher
                                ,Semister,Subject
                                ,Course,Post)

class UserRegistationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","password1","password2"]

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["name","description","due_fees"]

class TeacherCreationForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=["name","description","subject","due_salary"]


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=["name","description","teacher","student","semister"]


class SemisterCreationForm(forms.ModelForm):
    class Meta:
        model=Semister
        fields=["name","description","teacher","student","subject"]

class SubjectCreationForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields=["name","description","marks"]

class PostCreationForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title","description","user"]





