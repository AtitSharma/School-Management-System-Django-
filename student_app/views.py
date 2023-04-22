from django.shortcuts import render,redirect,reverse
from student_app.forms import (UserRegistationForm
                               ,StudentCreationForm,
                               TeacherCreationForm,
                               CourseCreationForm,
                               SemisterCreationForm,
                               SubjectCreationForm,PostCreationForm
                               )
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from student_app.models import Student,Teacher,Subject,Semister,School,Course,Post
from django.views.generic import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.


def home(request):
    return render(request,"student_app/home.html")



def student_home(request):
    posts=Post.objects.all()
    context={
       "posts":posts
    }
    return render(request,"student_app/student_home.html",context)


def admin_home(request):
    courses=Course.objects.all()
    teacher=Teacher.objects.all()
    student=Student.objects.all()
    context={
        "courses":courses,
        "teachers":teacher,
        "students":student
        }
    return render(request,"student_app/admin_home.html",context)

# def manage_course(request,pk):
#     course=Course.objects.filter(pk=pk)
#     context={
#         "courses":course
#     }

#     return render(request,"student_app/course_detail.html",context)



class Login(LoginView):
    template_name="student_app/login.html"


def student_login(request):
    form=AuthenticationForm(request.POST or None)
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user) 
            return HttpResponseRedirect(reverse("student:student_home"))
    return render(request,"student_app/student_login.html",{"form":form})



def manage(request,title):
    courses=Course.objects.all()
    students=Student.objects.all()
    teachers=Teacher.objects.all()
    subjects=Subject.objects.all()
    semisters=Semister.objects.all()
    schools=School.objects.all()


    if title=="course":
        return render(request,"student_app/manage.html",{"courses":courses,"title":title})
    elif title=="student":
        return render(request,"student_app/manage.html",{"students":students,"title":title})
    elif title=="teacher":
        return render(request,"student_app/manage.html",{"teachers":teachers,"title":title})
    elif title=="subject":
        return render(request,"student_app/manage.html",{"subjects":subjects,"title":title})
    elif title=="semister":
        return render(request,"student_app/manage.html",{"semisters":semisters,"title":title})
    elif title=="school":
        return render(request,"student_app/manage.html",{"schools":schools,"title":title})
        
    return render(request,"student_app/manage.html")

def register(request):
    form=UserRegistationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("student:home")
    context={"form":form}
    return render(request,"student_app/register.html",context)


def add_student(request):
    if request.method=="POST":
        form=StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:manage",title="student")
    else:
        form=StudentCreationForm()
    return render(request,"student_app/add_student.html",{"form":form})

def add_teacher(request):
    if request.method=="POST":
        form=TeacherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:manage",title="teacher")
    else:
        form=TeacherCreationForm()
    return render(request,"student_app/add_teacher.html",{"form":form})


def add_course(request):
    if request.method=="POST":
        form=CourseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:manage",title="course")
    else:
        form=CourseCreationForm()
    return render(request,"student_app/add_course.html",{"form":form})

def add_subject(request):
    if request.method=="POST":
        form=SubjectCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:manage",title="subject")
    else:
        form=SubjectCreationForm()
    return render(request,"student_app/add_subject.html",{"form":form})


def add_semister(request):
    if request.method=="POST":
        form=SemisterCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:manage",title="semister")
    else:
        form=SemisterCreationForm()
    return render(request,"student_app/add_semister.html",{"form":form})


class EditCourse(LoginRequiredMixin,UpdateView):
    model=Course
    fields=["name","description","teacher","student","semister"]
    template_name="student_app/edit_course.html"
    success_url=reverse_lazy("student:manage",args=["course"])

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Course.objects.get(pk=pk)
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context=super().get_context_data(**kwargs)
        context['pk']=pk
        return context
    

class EditStudent(LoginRequiredMixin,UpdateView):
    model=Student
    fields=["name","description","due_fees"]
    template_name="student_app/edit_student.html"
    success_url=reverse_lazy("student:manage",args=["student"])

    def get_object(self):
        pk=self.kwargs.get("pk")
        return Student.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context["pk"]=pk
        context["semister"]=Semister.objects.filter(pk=pk)
        return context

    
class EditSemister(LoginRequiredMixin,UpdateView):
    model=Semister
    fields=["name","description","teacher","student","subject"]
    template_name="student_app/edit_semister.html"
    success_url=reverse_lazy("student:manage",args=["semister"])

    def get_object(self):
        pk=self.kwargs.get("pk")
        return Semister.objects.get(pk=pk)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context["semisters"]=Semister.objects.filter(pk=pk)
        context['pk']=pk
        return context
    
class EditTeacher(LoginRequiredMixin,UpdateView):
    model=Teacher
    fields=["name","description","due_salary","subject"]
    template_name="student_app/edit_teacher.html"
    success_url=reverse_lazy("student:manage",args=["teacher"])

    def get_object(self):
        pk=self.kwargs.get("pk")
        return Teacher.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context["pk"]=pk
        return context



class EditSubject(LoginRequiredMixin,UpdateView):
    model=Subject
    fields=["name","description","marks"]
    template_name="student_app/edit_student.html"
    success_url=reverse_lazy("student:manage",args=["subject"])

    def get_object(self):
        pk=self.kwargs.get("pk")
        return Subject.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context["pk"]=pk
        return context


class DeleteStudent(LoginRequiredMixin,DeleteView):
    model=Student
    template_name="student_app/delete_student.html"

    def get_success_url(self):
        return reverse("student:manage",args=("student",))
    
class DeleteTeacher(LoginRequiredMixin,DeleteView):
    model=Teacher
    template_name="student_app/delete_teacher.html"

    def get_success_url(self):
        return reverse("student:manage",args=("teacher",))

class DeleteCourse(LoginRequiredMixin,DeleteView):
    model=Course
    template_name="student_app/delete_course.html"

    def get_success_url(self):
        return reverse("student:manage",args=("course",))
    
class DeleteSubject(LoginRequiredMixin,DeleteView):
    model=Subject
    template_name="student_app/delete_subject.html"

    def get_success_url(self):
        return reverse("student:manage",args=("subject",))
    
class DeleteSemister(LoginRequiredMixin,DeleteView):
    model=Semister
    template_name="student_app/delete_semister.html"

    def get_success_url(self):
        return reverse("student:manage",args=("semister",))
    

def create_post(request):
    if request.method=="POST":
        form=PostCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:student_home")
    else:
        form=PostCreationForm()
    return render(request,"student_app/add_post.html",{"form":form})













