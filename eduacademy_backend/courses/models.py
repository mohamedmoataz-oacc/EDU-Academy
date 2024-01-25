from django.db import models
from autoslug import AutoSlugField
from accounts.models import *

class Subject(models.Model):
    teachers = models.ManyToManyField(Teacher, through="Teaching")

    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.subject_name)
    
class Course(models.Model):
    students = models.ManyToManyField(Student, through="Enrollment")
    assistants = models.ManyToManyField(Assistant, through="Assisting")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    course_name = models.CharField(max_length=150)
    description = models.TextField()
    lecture_price = models.PositiveIntegerField()
    package_size = models.PositiveSmallIntegerField()
    thumbnail = models.ImageField(upload_to="courses/courses_thumbnails/")
    creation_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course_name} -> {self.teacher.teacher.username}'


class Assisting(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('assistant', 'course')
    
    start_date = models.DateTimeField(auto_now_add=True)

class CourseRating(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    course = models.ForeignKey(Course, models.CASCADE)
    class Meta:
        unique_together = ('student', 'course')
        constraints = [models.CheckConstraint(check=models.Q(rating__lte=5), name="course_rate_lte_5")]
        
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.course.course_name}: {self.rating}'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('student', 'course')

    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.student.username} -> {self.course.course_name}'

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('lecture_title', 'course')
        
    lecture_title = models.CharField(max_length=150)
    lecture_slug = AutoSlugField(populate_from='lecture_title')
    video = models.FileField(null=True, max_length=250)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.lecture_title} -> {self.course.course_name}'
    
class Teaching(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    teacher = models.ForeignKey(Teacher, models.CASCADE)

    class Meta:
        unique_together = ('subject', 'teacher')
