from django.db import models
# from django.contrib.auth.models import Permission,Group
from django.contrib.auth.models import AbstractUser,AbstractBaseUser


class User_Status(models.TextChoices):
    STUDENT="student","STUDENT"
    TEACHER="teacher","TEACHER"
    ADMIN ="admin","ADMIN"


class User(AbstractUser):

    status=models.CharField(max_length=100,choices=User_Status.choices,default=User_Status.STUDENT)
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    def __str__(self):
        return str(self.username)
    


class BaseModel(models.Model):
    start_at = models.DateField(auto_now_add=True)
    now_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        abstract=True
    
class Student(BaseModel):
    due_fees = models.IntegerField(blank=True, null=True, default=0)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="students",blank=True,null=True)
    USERNAME_FIELD="user__username"
    
    def __str__(self):
        return str(self.user.username)

class Subject(BaseModel):
    marks = models.IntegerField(blank=True, null=True, default=100)
    
    def __str__(self):
        return self.name
    


class Teacher(BaseModel):
    due_salary = models.IntegerField(blank=True, null=True, default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="teacher",blank=True,null=True)

    def __str__(self):
        return str(self.user.username)



class Semister(BaseModel):
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)
    subject=models.ManyToManyField(Subject)
    
    def __str__(self):
        return str(self.name)


class Course(BaseModel):
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField(Student)
    semister = models.ManyToManyField(Semister)

    def __str__(self):
        return str(self.name)
    

class School(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    


class Post(models.Model):
    title=models.CharField(max_length=250,blank=True,null=True)
    description=models.TextField()
    

    def __str__(self):
        return str(self.title)


class Message(models.Model):
    title=models.CharField(max_length=250,blank=True,null=True)
    description=models.TextField()
    

    def __str__(self):
        return str(self.title)
    

class AdmissionMessage(BaseModel):
    name=models.CharField(max_length=250)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="admission_message")
    contact_number=models.CharField(max_length=100)


    def __str__(self):
        return str(self.name)









