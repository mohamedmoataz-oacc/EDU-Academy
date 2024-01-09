from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser

class UsersRole(models.Model):
    role = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return str(self.role)

class PaymentMethod(models.Model):
    method = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return str(self.method)

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

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    notification_title = models.CharField(max_length=100)
    notification = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.notification_title)

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
    verified = models.BooleanField(default=False)
    personal_photo = models.ImageField(upload_to="students/personal_photos/", null=True, blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"

class Badge(models.Model):
    students = models.ManyToManyField(Student, through="BadgeEarning")

    badge_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.badge_name)

class BadgeEarning(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'badge')

class Teacher(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    balance = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=None, null=True, blank=True)
    personal_photo = models.ImageField(upload_to="teachers/personal_photos/")
    national_ID_photo = models.ImageField(upload_to="teachers/national_IDs/")

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"

class TeachRequest(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    date_submitted = models.DateTimeField(auto_now_add=True)
    date_reviewed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"

class TeacherBalanceTransaction(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.teacher.username}: {self.amount} | {self.transaction_date}"

class Subject(models.Model):
    teachers = models.ManyToManyField(Teacher, through="Teaching")

    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.subject_name)

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

    def __str__(self):
        return f'{self.teacher.teacher.username}: {self.rating}'

class Assistant(models.Model):
    assistant = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    personal_photo = models.ImageField(upload_to="assistants/personal_photos/")
    national_ID_photo = models.ImageField(upload_to="assistants/national_IDs/")

    def __str__(self):
        return f"{self.assistant.first_name} {self.assistant.last_name}"

class AssistanceRequest(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)

    message = models.TextField()
    accepted = models.BooleanField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assistant.assistant.username} -> {self.teacher.teacher.username}"

class AssistantRating(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    assistant = models.ForeignKey(Assistant, models.CASCADE)
    class Meta:
        unique_together = ('student', 'assistant')
        constraints = [models.CheckConstraint(check=models.Q(rating__lte=5), name="assistant_rate_lte_5")]
        
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.assistant.assistant.username}: {self.rating}'

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

class Warnings(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    warning_title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.warning_title)

class Attachment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    
    attachment = models.FileField(null=True, max_length=250, upload_to="lectures/attachments/")

    def __str__(self):
        return str(self.attachment)

class Payment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "lecture")

    def __str__(self):
        return f'{self.student.student.username} -> {self.lecture.lecture_title}'

class PointsTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.student.username}: {self.amount} | {self.transaction_date}'

class StudentBalanceTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.student.username}: {self.amount} | {self.transaction_date}'

class Quiz(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE)

    duration_in_minutes = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()

    def __str__(self):
        return f'{self.lecture.lecture_title}: {self.start_date}'

class QuizHandIn(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('student', 'quiz')

    mark = models.PositiveSmallIntegerField()
    is_marked = models.BooleanField(default=False)
    hand_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        to_return = f'{self.student.student.username}'
        if self.is_marked:
            to_return += f': {self.mark}'
        return to_return

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question = models.TextField()

    def __str__(self):
        to_return = str(self.question)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return

class QuizQuestionChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)

    choice = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        to_return = str(self.choice)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return + f' | {self.is_correct}'

class QuizQuestionAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)
    student = models.ForeignKey(Student, models.CASCADE)
    class Meta:
        unique_together = ('student', 'question')
    
    answer = models.TextField()

    def __str__(self):
        to_return = str(self.answer)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return

class Assignment(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE)

    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.lecture.lecture_title}: {self.upload_date}'

class AssignmentHandIn(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('student', 'assignment')

    mark = models.PositiveSmallIntegerField()
    is_marked = models.BooleanField(default=False)
    hand_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        to_return = f'{self.student.student.username}'
        if self.is_marked:
            to_return += f': {self.mark}'
        return to_return

class AssignmentQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    question = models.TextField()

    def __str__(self):
        to_return = str(self.question)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return

class AssignmentQuestionChoice(models.Model):
    question = models.ForeignKey(AssignmentQuestion, models.CASCADE)

    choice = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        to_return = str(self.choice)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return + f' | {self.is_correct}'

class AssignmentQuestionAnswer(models.Model):
    question = models.ForeignKey(AssignmentQuestion, models.CASCADE)
    student = models.ForeignKey(Student, models.CASCADE)
    class Meta:
        unique_together = ('student', 'question')
    
    answer = models.TextField()

    def __str__(self):
        to_return = str(self.answer)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return

class QA(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    question = models.TextField()
    closed = models.BooleanField(default=False)
    question_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.student.username} -> {self.lecture.lecture_title} | {self.closed}"

class QAAnswer(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qa = models.ForeignKey(QA, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through="Upvote")

    answer = models.TextField()
    upvotes = models.PositiveSmallIntegerField(default=0)
    marked_correct = models.BooleanField(default=False)
    answer_date = models.DateField(auto_now_add=True)

    def __str__(self):
        to_return = str(self.answer)
        if len(to_return > 100): to_return = to_return[:97] + '...'
        return to_return + f": {self.upvotes} | {self.marked_correct}"

class Upvote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.ForeignKey(QAAnswer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'answer')