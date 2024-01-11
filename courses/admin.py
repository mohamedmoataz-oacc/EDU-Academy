from django.contrib import admin
from .models import *

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assisting)
admin.site.register(CourseRating)
admin.site.register(Lecture)
admin.site.register(Teaching)