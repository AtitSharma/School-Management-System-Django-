from django.contrib import admin

# Register your models here.

from student_app.models import Student,Teacher,Subject,Semister,Course,School
admin.site.register(School)
admin.site.register(Course)
admin.site.register(Semister)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)




