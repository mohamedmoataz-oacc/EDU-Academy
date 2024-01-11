from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    notification_title = models.CharField(max_length=100)
    notification = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.notification_title)

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

class TeacherBalanceTransaction(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.teacher.username}: {self.amount} | {self.transaction_date}"

class TeacherRating(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    teacher = models.ForeignKey(Teacher, models.CASCADE)
    class Meta:
        unique_together = ('student', 'teacher')
        constraints = [models.CheckConstraint(check=models.Q(rating__lte=5), name="teacher_rate_lte_5")]
        
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.teacher.teacher.username}: {self.rating}'

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