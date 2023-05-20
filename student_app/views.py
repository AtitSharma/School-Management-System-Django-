from django.shortcuts import render,redirect,reverse
from student_app.forms import (UserRegistationForm
                               ,StudentCreationForm,
                               TeacherCreationForm,
                               CourseCreationForm,
                               SemisterCreationForm,
                               SubjectCreationForm,PostCreationForm,AdmissionForm,MessageForm,StudentLoginForm,
                               )
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from student_app.models import Student,Teacher,User,Subject,Semister,School,Course,Post,AdmissionMessage,Message
from django.views.generic import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from embed_video.backends import detect_backend
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from student_home import settings
from celery import shared_task
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


# from student_app.tasks import send_mail_func


class SuperUserRequiredMixins(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
        


def home(request):
    video_url = "https://www.youtube.com/watch?v=KZNDqHI8AW4&list=RDKZNDqHI8AW4&start_radio=1"
    backend = detect_backend(video_url)
    context = {
        'video_url': video_url,
        'backend': backend,
    }
    return render(request,"student_app/home.html",context)


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
            pk=int(request.POST.get("user"))
            form.save()
            User.objects.filter(pk=pk).update(status="student")
            messages.success(request,"Student added sucessfully")
            return redirect("student:admin_home")
    else:
        form=StudentCreationForm()
    return render(request,"student_app/add_student.html",{"form":form})

@user_passes_test(lambda u:u.is_superuser)
def add_teacher(request):
    if request.method=="POST":
        form=TeacherCreationForm(request.POST)
        if form.is_valid():
            teacher=request.POST.get("name")
            pk=int(request.POST.get("user"))
            print(pk)
            form.save()
            User.objects.filter(pk=pk).update(status="teacher")
            messages.success(request,"sucessfully added")
            return redirect("student:admin_home")
        
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
            return redirect("student:admin_home")
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
            return redirect("student:admin_home")
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
            return redirect("student:admin_home")
    else:
        form=SemisterCreationForm()
    return render(request,"student_app/add_semister.html",{"form":form})


class EditCourse(LoginRequiredMixin,UpdateView):
    model=Course
    fields=["name","description","teacher","student","semister"]
    template_name="student_app/edit_course.html"
    success_url=reverse_lazy("student:admin_home")

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
    success_url=reverse_lazy("student:admin_home")

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
    success_url=reverse_lazy("student:admin_home")

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
    success_url=reverse_lazy("student:admin_home")

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
    success_url=reverse_lazy("student:admin_home")

    def get_object(self):
        pk=self.kwargs.get("pk")
        messages.success(self.request,"sucessfully updated")
        return Subject.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        
        pk=self.kwargs.get("pk")
        context["pk"]=pk
        return context


@user_passes_test(lambda u:u.is_superuser)
def delete_student(request,pk):
    student=Student.objects.get(pk=pk)
    student.delete()
    return redirect("student:admin_home")
   
@user_passes_test(lambda u:u.is_superuser) 
def delete_teacher(request,pk):
    teacher=Teacher.objects.get(pk=pk)
    teacher.delete()
    return redirect("student:admin_home")

@user_passes_test(lambda u:u.is_superuser)
def delete_course(request,pk):
    course=Course.objects.get(pk=pk)
    course.delete()
    return redirect("student:admin_home")
   
@user_passes_test(lambda u:u.is_superuser) 
def delete_subject(request,pk):
    subject=Subject.objects.get(pk=pk)
    subject.delete()
    return redirect("student:admin_home")
 
@user_passes_test(lambda u:u.is_superuser)   
def delete_semister(request,pk):
    semister=Semister.objects.get(pk=pk)
    semister.delete()
    messages.add_message(request,messages.INFO,"Deleted sucessfully")
    return redirect("student:admin_home")


    
@user_passes_test(lambda u:u.is_superuser)
def create_post(request):
    if request.method=="POST":
        form=PostCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("***************************************************************************************")
            mail_subject=request.POST.get("title")
            message=request.POST.get("description")
            send_mails_to_all(request,mail_subject,message)
            return redirect("student:admin_home")
    else:
        form=PostCreationForm()
    return render(request,"student_app/add_post.html",{"form":form})


class EditPost(SuperUserRequiredMixins,UpdateView):
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

@user_passes_test(lambda u:u.is_superuser)
def delete_post(request,pk):
    post=Post.objects.get(pk=pk)
    post.delete()
    return redirect("student:admin_home")



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



class ProfileUpdateStudent(SuperUserRequiredMixins,UserPassesTestMixin,UpdateView):
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




@shared_task
def send_mails_to_all(request,mail_subject,message):   
    users=get_user_model().objects.all()
    mes=message
    for user in users:
        to_email=user.email
        message = render_to_string("student_app/show_in_all.html", {
        'title':mes,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
        })
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return HttpResponse("SENT")
    



def search(request):
    query=request.GET['query']
    # std1=Student.objects.filter(name__icontains=query)
    # std2=Student.objects.filter(description__icontains=query)
    # students=std1.union(std2)
    students=Student.objects.filter(name__icontains=query)| Student.objects.filter(description__icontains=query)
    context={
       "students":students,
        
    }

    return render(request,"student_app/search.html",context)








        
    










