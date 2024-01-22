from django.db import models
from accounts.models import Teacher, Student

class TeachRequest(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    date_submitted = models.DateTimeField(auto_now_add=True)
    date_reviewed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"

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