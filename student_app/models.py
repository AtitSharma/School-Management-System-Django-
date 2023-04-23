from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # user_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    def __str__(self):
        return str(self.id)

class BaseModel(models.Model):
    start_at = models.DateField(auto_now_add=True)
    now_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        abstract=True

    
class Student(User,BaseModel):
    due_fees = models.IntegerField(blank=True, null=True, default=0)
    def __str__(self):
        return self.username

class Subject(BaseModel):
    marks = models.IntegerField(blank=True, null=True, default=100)

    def __str__(self):
        return self.name
    


class Teacher(User,BaseModel):
    due_salary = models.IntegerField(blank=True, null=True, default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.username



class Semister(BaseModel):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    semister = models.ForeignKey(Semister, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name
    

class School(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    


class Post(models.Model):
    title=models.CharField(max_length=250,blank=True,null=True)
    description=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")

    def __str__(self):
        return self.title


class Message(models.Model):
    title=models.CharField(max_length=250,blank=True,null=True)
    description=models.TextField()
    

    def __str__(self):
        return self.title
    

class AdmissionMessage(BaseModel):
    name=models.CharField(max_length=250,blank=True,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="admission_message")
    contact_number=models.IntegerField()

class Admin(User,models.Model):

    def __str__(self):
        return self.username







