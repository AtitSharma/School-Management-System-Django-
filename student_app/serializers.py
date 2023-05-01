from rest_framework import serializers


from student_app.models import Student,Teacher



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=["name","description","user","due_salary","subject"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=["name","description"]