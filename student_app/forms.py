from django import forms
from django.contrib.auth.forms import UserCreationForm
from student_app.models import User,Student,Teacher,Semister,Subject




class UserRegistationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","password1","password2"]

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["name","description","due_fees"]
