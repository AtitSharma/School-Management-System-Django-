from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from student_app.models import (User
                                ,Student,Teacher
                                ,Semister,Subject
                                ,Course,Post,AdmissionMessage,Message)

class UserRegistationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["name","description","due_fees","user"]
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]="form-control"

class TeacherCreationForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=["name","description","subject","due_salary","user"]


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
        fields=["title","description"]


class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=["title","description"]


class AdmissionForm(forms.ModelForm):
    class Meta:
        model=AdmissionMessage
        fields=["name","course","contact_number"]

class StudentProfileManagementForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["name","description"]




class StudentRegistationForm(UserCreationForm):
    class Meta:
        model=Student
        fields=["name","password1","password2"]




class StudentLoginForm(AuthenticationForm):
    class Meta:
        model=Student
        fields=["name","password1","password2"]












