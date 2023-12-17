from django.db import models
from django.contrib.auth.models import AbstractUser

class UsersRole(models.Model):
    role = models.CharField(max_length=15, unique=True)

class User(AbstractUser):
    gender_choices = [("M", "Male"), ("F", "Female")]

    user_role = models.ForeignKey(UsersRole, on_delete=models.CASCADE)

    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=gender_choices)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    governorate = models.CharField(max_length=20)
    phone_number = models.IntegerField()

    def __str__(self):
        return f'{User.username}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    notification = models.TextField()
    notification_date = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    academic_year_choices = ([(i, f"Junior {i}") for i in range(1, 7)] + 
                            [(i - 6, f"Middle {i}") for i in range(7, 10)] +
                            [(i - 9, f"Senior {i}") for i in range(10, 13)])
    study_field_choices = [(0, "3elmy 3loom"), (1, "3elmy reyada"), (2, "Adaby")]
    
    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    birth_date = models.DateField()
    academic_year = models.CharField(max_length=10, choices=academic_year_choices)
    study_field = models.CharField(max_length=15, choices=study_field_choices, null=True, blank=True)
    parent_phone_number = models.IntegerField()
    parent_name = models.CharField(max_length=60)
    points = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
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
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    balance = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=None, null=True, blank=True)
    personal_photo = models.ImageField(null=True, blank=True)
    national_ID_photo = models.ImageField(null=True, blank=True)

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
    assistant = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    birth_date = models.DateField()
    personal_photo = models.ImageField(null=True, blank=True)
    national_ID_photo = models.ImageField(null=True, blank=True)

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
    assistants = models.ManyToManyField(Assistant, through="Assisting")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    course_name = models.CharField(max_length=150)
    description = models.TextField()
    lecture_price = models.PositiveIntegerField()
    package_size = models.PositiveSmallIntegerField()
    thumbnail = models.ImageField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

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

class Quiz(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    duration_in_minutes = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()

class QuizHandIn(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('student', 'quiz')

    mark = models.PositiveSmallIntegerField()
    is_marked = models.BooleanField(default=False)
    hand_in = models.DateTimeField(auto_now_add=True)

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question = models.TextField()

class QuizQuestionChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)

    choice = models.TextField()
    is_correct = models.BooleanField(default=False)

class QuizQuestionAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)
    student = models.ForeignKey(Student, models.CASCADE)
    class Meta:
        unique_together = ('student', 'question')
    
    answer = models.TextField()

class Assignment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    upload_date = models.DateTimeField(auto_now_add=True)

class AssignmentHandIn(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('student', 'assignment')

    mark = models.PositiveSmallIntegerField()
    is_marked = models.BooleanField(default=False)
    hand_in = models.DateTimeField(auto_now_add=True)

class AssignmentQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    question = models.TextField()

class AssignmentQuestionChoice(models.Model):
    question = models.ForeignKey(AssignmentQuestion, models.CASCADE)

    choice = models.TextField()
    is_correct = models.BooleanField(default=False)

class AssignmentQuestionAnswer(models.Model):
    question = models.ForeignKey(AssignmentQuestion, models.CASCADE)
    student = models.ForeignKey(Student, models.CASCADE)
    class Meta:
        unique_together = ('student', 'question')
    
    answer = models.TextField()

class QA(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    question = models.TextField()
    closed = models.BooleanField(default=False)
    question_date = models.DateTimeField(auto_now_add=True)

class QAAnswer(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qa = models.ForeignKey(QA, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through="Upvote")

    answer = models.TextField()
    upvotes = models.PositiveSmallIntegerField(default=0)
    marked_correct = models.BooleanField(default=False)
    answer_date = models.DateField(auto_now_add=True)

class Upvote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.ForeignKey(QAAnswer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'answer')