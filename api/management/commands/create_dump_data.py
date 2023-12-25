from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async

from api.models import *

import random
from datetime import date, timedelta
import asyncio
from tqdm import tqdm

class Command(BaseCommand):
    help = 'a command to create dump data'
    def handle(self, *args, **options):
        # Your command logic goes here
        self.stdout.write(self.style.SUCCESS('your command ran successfully.'))

governorates = [
    "Cairo", "Alexandria", "Giza", "Shubra El-Kheima", "Port Said", "Suez",
    "Luxor", "Asyut", "Mansoura", "Tanta", "Fayoum", "Zagazig", "Ismailia",
    "Kafr El Sheikh", "Assiut", "Damanhur", "El Mahalla El Kubra", "Banha",
    "Qena", "Sohag", "Hurghada", "Beni Suef", "Damietta", "Minya", "Quesna",
    "Shibin El Kom", "Siwa Oasis", "Arish", "Marsa Matruh"
]

male_names = [
    "Hisham", "Maged", "Osama", "Hamza", "Fadi", "Ibrahim", "Rami", "Yassin", "Moustafa", "Mohsen",
    "Hazem", "Fahim", "Magdi", "Nader", "Walid", "Raafat", "Samir", "Nabil", "Zakaria", "Tamer",
    "Ahmed", "Mohamed", "Mahmoud", "Amr", "Ali", "Omar", "Tarek", "Khaled", "Hossam", "Ayman",
    "Adel", "Sherif", "Wael", "Ashraf", "Karim", "Essam", "Mostafa", "Youssef", "Sayed", "Kareem",
    "Wael", "Hani", "Firas", "Mazen", "Kamal", "Hassan", "Sameh", "Yahya", "Majid", "Bassam", 
    "Riad", "Anwar", "Ziad", "Mamdouh", "Tariq", "Khalid", "Ahmad", "Sami", "Kassem",
    "Ezzat", "Mohsen", "Sharif", "Mustafa", "Wassim", "Makram", "Ismail", "Rami", "Amin"
]

female_names = [
    "Aya", "Nour", "Lama", "Fatma", "Sara", "Hana", "Mona", "Reem", "Yasmine", "Hoda",
    "Mai", "Dina", "Salma", "Nada", "Rania", "Shaimaa", "Amira", "Dalia", "Heba", "Jasmine",
    "Marwa", "Nadia", "Rasha", "Farida", "Nermeen", "Eman", "Naglaa", "Noha", "Ghada", "Yara",
    "Shorouk", "Shereen", "Doha", "Asmaa", "Zeinab", "Hayam", "Mervat", "Ola", "Maha", "Raghad",  
    "Lina", "Dalia", "Leila", "Layla", "Maya", "Noura", "Zainab", "Safia", "Inas", "Yara",
    "Rawan", "Rabab", "Maha", "Raghad", "Mervat", "Hayam", "Mona", "Nada", "Rasha", "Jana",
    "Dalal", "Batoul", "Laila", "Nisreen", "Sama",
]

genders = ["M", "F"]

roles = ["Admin", "Student", "Teacher", "Assistant"]

subjects = ["Arabic", "Math", "English", "French"]

def generate_random_birth_date(start_date, end_date):
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def create_users_roles():
    print("Creating user roles...")
    for role in roles:
        UsersRole.objects.create(role=role)

def create_payment_methods():
    print("Creating payment methods...")
    methods = ["balance", "points"]
    for method in methods:
        PaymentMethod.objects.create(method=method)

def create_users(created_users=50):
    print("Creating users...")
    for _ in tqdm(range(created_users)):
        gender = random.choice(["M", "F"])
        first_name = random.choice(male_names) if gender == "M" else random.choice(female_names)
        last_name = random.choice(male_names)
        username = first_name + str(_) + last_name
        password = username
        role = UsersRole.objects.get(role=random.choice(roles))
        email = username+"@yahoo.com"
        governorate = random.choice(governorates)
        phone_number = random.randint(1000000000, 1999999999)
        if role.role == "Admin" or role.role == "Teacher":
            rand_BD = generate_random_birth_date(date(1960, 1, 1), date(1980, 1, 1))
        elif role.role == "Assistant":
            rand_BD = generate_random_birth_date(date(1995, 1, 1), date(2003, 1, 1))
        else:
            rand_BD = generate_random_birth_date(date(2004, 1, 1), date(2015, 1, 1))

        if role.role == "Admin":
            User.objects.create_superuser(
                user_role=role,
                email=email,
                gender=gender,
                first_name=first_name,
                last_name=last_name,
                governorate=governorate,
                phone_number=phone_number,
                birth_date=rand_BD,
                username=username,
                password=password
            )
        else:
            User.objects.create_user(
                user_role=role,
                email=email,
                gender=gender,
                first_name=first_name,
                last_name=last_name,
                governorate=governorate,
                phone_number=phone_number,
                birth_date=rand_BD,
                username=username,
                password=password
            )

def create_teachers():
    print("Creating teachers (also creates their courses) ...")
    create_teacher = Teacher.objects.create
    for user in tqdm(User.objects.filter(user_role__role="Teacher")):
        id_path = "teachers/id.jpeg"
        personal_photo_path = "teachers/personal.jpg"
        
        t = create_teacher(
            teacher = user,
            balance = 0,
            accepted = True,
            personal_photo = personal_photo_path,
            national_ID_photo = id_path
        )
        
        subject_created = Subject.objects.get(subject_name = random.choice(subjects))
        subject_created.teachers.add(t)

        course_created = create_course(t, subject_created)
        create_lectures(course_created)


def create_subjects():
    print("Creating subjects...")
    for subject_name in subjects:
        Subject.objects.create(subject_name = subject_name)

def create_course(teacher: Teacher, subject : Subject):
    c = Course.objects.create(
        teacher = teacher,
        subject = subject,
        course_name = subject.subject_name+"->"+str(teacher.teacher.pk),
        description = f"{subject.subject_name} by {teacher.teacher.first_name} {teacher.teacher.last_name}",
        lecture_price = random.choice([40, 50, 60, 70, 80, 90]),
        package_size = random.choice([2, 3, 4, 5, 6]),
        thumbnail = f"courses/courses_thumbnails/{subject.subject_name}/1.jpeg"
    )
    return c

def create_lectures(course:Course):
    for i in range(random.randint(1, 10)):
        Lecture.objects.create(
            course=course,
            lecture_title = course.subject.subject_name+str(course.pk)+ " lec" +str(i),
            video = "courses/videos/1.mp4"
        )

create_users_roles()
create_subjects()
create_payment_methods()
create_users()
create_teachers()