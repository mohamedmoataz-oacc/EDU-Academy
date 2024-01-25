from django.db import models
from accounts.models import Teacher, Student
from courses.models import Course, Lecture

class PaymentMethod(models.Model):
    method = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return str(self.method)


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
