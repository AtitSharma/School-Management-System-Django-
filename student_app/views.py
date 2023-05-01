from django.shortcuts import render,redirect,reverse
from student_app.forms import (UserRegistationForm
                               ,StudentCreationForm,
                               TeacherCreationForm,
                               CourseCreationForm,
                               SemisterCreationForm,
                               SubjectCreationForm,PostCreationForm,AdmissionForm,MessageForm,StudentLoginForm,
                               )

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from student_app.models import Student,Teacher,User,Subject,Semister,School,Course,Post,AdmissionMessage,Message
from django.views.generic import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test





def home(request):
    return render(request,"student_app/home.html")


@login_required
def student_home(request):
    posts=Post.objects.all()
    pk=User.objects.filter(pk=request.user.id)

    context={
       "posts":posts,
       "pk":pk
    }
    return render(request,"student_app/student_home.html",context)

@user_passes_test(lambda u:u.is_superuser)
def admin_home(request):
    courses=Course.objects.all()
    teacher=Teacher.objects.all()
    student=Student.objects.all()
    posts=Post.objects.all()
    complaints=Message.objects.all()
    subjects=Subject.objects.all()
    semisters=Semister.objects.all()
    admission_message=AdmissionMessage.objects.all()


    context={
        "courses":courses,
        "teachers":teacher,
        "students":student,
        "posts":posts,
        "complaints":complaints,
        "admisssion_message":admission_message,
        "subjects":subjects,
        "semisters":semisters

        }
    return render(request,"student_app/admin_home.html",context)


class Login(LoginView):
    template_name="student_app/login.html"
    


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("student:home"))
    

@user_passes_test(lambda u:u.is_superuser)
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
    messages.success(request,f"Sucessfully edited {title}")
    return render(request,"student_app/manage.html")

def register(request):
    form=UserRegistationForm(request.POST)
    if form.is_valid():
        form.save() 
        return redirect("student:home")
    
    context={"form":form}
    return render(request,"student_app/student_register.html",context)

@user_passes_test(lambda u:u.is_superuser)
def add_student(request):
    if request.method=="POST":
        form=StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Student added sucessfully")
            return redirect("student:manage",title="student")
    else:
        form=StudentCreationForm()
    return render(request,"student_app/add_student.html",{"form":form})

@user_passes_test(lambda u:u.is_superuser)
def add_teacher(request):
    teacher=request.POST.get("name")
    print(teacher,"****************************************")
    if request.method=="POST":
        form=TeacherCreationForm(request.POST)
        
        if form.is_valid():
            teacher=request.POST.get("name")
            print(teacher)

            form.save()
            messages.success(request,"sucessfully added")
            return redirect("student:manage",title="teacher")
    else:
        form=TeacherCreationForm()
    return render(request,"student_app/add_teacher.html",{"form":form})

@user_passes_test(lambda u:u.is_superuser)
def add_course(request):
    if request.method=="POST":
        form=CourseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"sucessfully added")
            return redirect("student:manage",title="course")
    else:
        form=CourseCreationForm()
    return render(request,"student_app/add_course.html",{"form":form})

@user_passes_test(lambda u:u.is_superuser)
def add_subject(request):
    if request.method=="POST":
        form=SubjectCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"sucessfully added")
            return redirect("student:manage",title="subject")
    else:
        form=SubjectCreationForm()
    return render(request,"student_app/add_subject.html",{"form":form})

@user_passes_test(lambda u:u.is_superuser)
def add_semister(request):
    if request.method=="POST":
        form=SemisterCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"sucessfully added")
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
        messages.success(self.request,"sucessfully updated")
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
        messages.success(self.request,"sucessfully updated")
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
        messages.success(self.request,"sucessfully updated")
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
        messages.success(self.request,"sucessfully updated")
        return Teacher.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context["pk"]=pk
        return context



class EditSubject(LoginRequiredMixin,UpdateView):
    model=Subject
    fields=["name","description","marks"]
    template_name="student_app/edit_subject.html"
    success_url=reverse_lazy("student:manage",args=["subject"])

    def get_object(self):
        pk=self.kwargs.get("pk")
        messages.success(self.request,"sucessfully updated")
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
    
@user_passes_test(lambda u:u.is_superuser)
def create_post(request):
    if request.method=="POST":
        form=PostCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student:admin_home")
    else:
        form=PostCreationForm()
    return render(request,"student_app/add_post.html",{"form":form})


class EditPost(LoginRequiredMixin,UpdateView):
    model=Post
    template_name="student_app/edit_post.html"
    fields=["title","description"]
    success_url=reverse_lazy("student:admin_home")


    def get_object(self):
        pk=self.kwargs.get("pk")
        return Post.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context["pk"]=pk
        return context

class DeletePost(LoginRequiredMixin,DeleteView):
    model=Post
    template_name="student_app/delete_post.html"
    def get_success_url(self):
        return reverse("student:admin_home")



def contact(request):
    return render(request,"student_app/contact.html")

def contact_for_message(request):
    if request.method=="POST":
        form=MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"We got your your message. We will look into it !!")
            return redirect("student:home")
    else:
        form=MessageForm()
    return render(request,"student_app/contact_complaint.html",{"form":form})

def contact_for_admission(request):
    if request.method=="POST":
        form=AdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"We got your your message for admission . We will contact you soon !!")
            return redirect("student:home")
    else:
        form=AdmissionForm()
    return render(request,"student_app/contact_admission.html",{"form":form})



class ProfileUpdateStudent(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=User
    fields=["username"]
    template_name="student_app/edit_studentprofile.html"
    success_url=reverse_lazy("student:student_home")
    

    def form_valid(self, form):
        form.instance.name= self.request.user.username

        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user.username==post.username:
            return True
        return False


    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get("pk")
        context['pk']=pk

        # print(self.request.user)
        return context

@user_passes_test(lambda u:u.is_superuser)
def view_complaints(request):
    complaints=Message.objects.all()
    return render(request,"student_app/view_complaints.html",{"complaints":complaints})

@user_passes_test(lambda u:u.is_superuser)
def view_admission(request):
    admission_message=AdmissionMessage.objects.all()
    return render(request,"student_app/view_admission.html",{"admission_message":admission_message})













        
    










