from django.db import models
# from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser

class UsersRole(models.Model):
    role = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return str(self.role)

class User(AbstractUser):
    gender_choices = [("M", "Male"), ("F", "Female")]

    user_role = models.ForeignKey(UsersRole, on_delete=models.CASCADE)

    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=gender_choices)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=40)
    governorate = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    birth_date = models.DateField()

    def save(self, *args, **kwargs):
        self.full_name = self.first_name + ' ' + self.last_name
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.username)
    
class Student(models.Model):
    academic_year_choices = ([(i, f"Junior {i}") for i in range(1, 7)] + 
                            [(i, f"Middle {i - 6}") for i in range(7, 10)] +
                            [(i, f"Senior {i - 9}") for i in range(10, 13)])
    study_field_choices = [(0, "3elmy 3loom"), (1, "3elmy reyada"), (2, "Adaby")]

    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    academic_year = models.SmallIntegerField(choices=academic_year_choices)
    study_field = models.SmallIntegerField(choices=study_field_choices, null=True, blank=True)
    parent_phone_number = models.IntegerField()
    parent_name = models.CharField(max_length=60)
    points = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    personal_photo = models.ImageField(upload_to="students/personal_photos/", null=True, blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"

class Teacher(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    balance = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=None, null=True, blank=True)
    personal_photo = models.ImageField(upload_to="teachers/personal_photos/")
    national_ID_photo = models.ImageField(upload_to="teachers/national_IDs/")

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"

class Assistant(models.Model):
    assistant = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    personal_photo = models.ImageField(upload_to="assistants/personal_photos/")
    national_ID_photo = models.ImageField(upload_to="assistants/national_IDs/")

    def __str__(self):
        return f"{self.assistant.first_name} {self.assistant.last_name}"
