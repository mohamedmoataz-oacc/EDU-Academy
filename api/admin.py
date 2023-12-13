from django.contrib import admin
from .models import *

admin.site.register(Users_role)
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TeachRequest)
admin.site.register(TeacherBalanceTransaction)
admin.site.register(Assistant)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Enrollment)