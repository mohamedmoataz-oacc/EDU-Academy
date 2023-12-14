from django.db import models

class UsersRole(models.Model):
    role = models.CharField(max_length=15)

class User(models.Model):
    user_role = models.ForeignKey(UsersRole, on_delete=models.CASCADE)

    email = models.EmailField()
    password = models.CharField(max_length=64)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    notification = models.TextField()
    notification_date = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    gender_choices = [("M", "Male"), ("F", "Female")]
    academic_year_choices = ([(i, f"Junior {i}") for i in range(1, 7)] + 
                            [(i - 6, f"Middle {i}") for i in range(7, 10)] +
                            [(i - 9, f"Senior {i}") for i in range(10, 13)])
    study_field_choices = [(0, "3elmy 3loom"), (1, "3elmy reyada"), (2, "Adaby")]
    
    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20, null=True, blank=True)
    lname = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=gender_choices)
    birth_date = models.DateField()
    academic_year = models.CharField(max_length=10, choices=academic_year_choices)
    study_field = models.CharField(max_length=15, choices=study_field_choices, null=True, blank=True)
    governorate = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    parent_phone_number = models.IntegerField()
    parent_name = models.CharField(max_length=60)
    points = models.IntegerField()
    balance = models.IntegerField()
    verified = models.BooleanField(default=False)
    personal_photo = models.ImageField(null=True, blank=True)

class PointsTransaction(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)

    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

class StudentBalanceTransaction(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)

    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

class Badge(models.Model):
    students = models.ManyToManyField(Student, through="BadgeEarning")

    badge_name = models.CharField(max_length=100)

class BadgeEarning(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'badge')

class Teacher(models.Model):
    gender_choices = [("M", "Male"), ("F", "Female")]
    
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20, null=True, blank=True)
    lname = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=gender_choices)
    governorate = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    balance = models.PositiveIntegerField()
    accepted = models.BooleanField()
    personal_photo = models.ImageField()
    national_ID_photo = models.ImageField()

class TeachRequest(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    date_submitted = models.DateTimeField(auto_now_add=True)
    date_reviewed = models.DateTimeField()

class TeacherBalanceTransaction(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

class Subject(models.Model):
    teachers = models.ManyToManyField(Teacher, through="Teaching")

    subject_name = models.CharField(max_length=50)

class Teaching(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    teacher = models.ForeignKey(Teacher, models.CASCADE)

    class Meta:
        unique_together = ('subject', 'teacher')

class TeacherRating(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    teacher = models.ForeignKey(Teacher, models.CASCADE)
    class Meta:
        unique_together = ('student', 'teacher')
        constraints = [models.CheckConstraint(check=models.Q(rating__lte=5), name="teacher_rate_lte_5")]
        
    rating = models.PositiveSmallIntegerField()

class Assistant(models.Model):
    gender_choices = [("M", "Male"), ("F", "Female")]
    
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20, null=True, blank=True)
    lname = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=gender_choices)
    governorate = models.CharField(max_length=20)
    birth_date = models.DateField()
    phone_number = models.IntegerField()
    personal_photo = models.ImageField()
    national_ID_photo = models.ImageField()

class AssistanceRequest(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)

    message = models.TextField()
    accepted = models.BooleanField()
    date_sent = models.DateTimeField(auto_now_add=True)

class AssistantRating(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    assistant = models.ForeignKey(Assistant, models.CASCADE)
    class Meta:
        unique_together = ('student', 'assistant')
        constraints = [models.CheckConstraint(check=models.Q(rating__lte=5), name="assistant_rate_lte_5")]
        
    rating = models.PositiveSmallIntegerField()

class Course(models.Model):
    students = models.ManyToManyField(Student, through="Enrollment")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    course_name = models.CharField(max_length=150)
    description = models.TextField()
    lecture_price = models.PositiveIntegerField()
    package_size = models.PositiveSmallIntegerField()
    thumbnail = models.ImageField()
    creation_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

class CourseRating(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    course = models.ForeignKey(Course, models.CASCADE)
    class Meta:
        unique_together = ('student', 'course')
        constraints = [models.CheckConstraint(check=models.Q(rating__lte=5), name="course_rate_lte_5")]
        
    rating = models.PositiveSmallIntegerField()

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('student', 'course')

    start_date = models.DateTimeField(auto_now_add=True)

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    lecture_title = models.CharField(max_length=150)
    video_path = models.CharField(max_length=250)
    upload_date = models.DateTimeField(auto_now_add=True)

class Warnings(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    date_sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

class Attachment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    
    attachment_path = models.CharField(max_length=250)

class Payment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveSmallIntegerField()

