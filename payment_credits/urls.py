from django.urls import path
from .views import *

app_name = "payment_credits"
urlpatterns = [
    path('payments/lectures/<int:lecture_id>/', pay_for_lecture, name='pay_for_lecture'),
]