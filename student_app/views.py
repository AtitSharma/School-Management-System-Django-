from django.shortcuts import render,redirect,reverse
from student_app.forms import UserRegistationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from student_app.models import Student,Teacher,Subject,Semister,School,Course
# Create your views here.


def home(request):
    return render(request,"student_app/home.html")



def student_home(request):
    return render(request,"student_app/student_home.html")

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



