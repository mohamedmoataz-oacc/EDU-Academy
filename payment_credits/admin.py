from django.contrib import admin
from .models import *

admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(PointsTransaction)
admin.site.register(StudentBalanceTransaction)