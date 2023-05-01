# Generated by Django 4.1.6 on 2023-04-28 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0002_alter_semister_student_alter_semister_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semister',
            name='student',
            field=models.ManyToManyField(blank=True, null=True, to='student_app.student'),
        ),
        migrations.AlterField(
            model_name='semister',
            name='subject',
            field=models.ManyToManyField(blank=True, null=True, to='student_app.subject'),
        ),
        migrations.AlterField(
            model_name='semister',
            name='teacher',
            field=models.ManyToManyField(blank=True, null=True, to='student_app.teacher'),
        ),
    ]
