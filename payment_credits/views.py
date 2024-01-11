from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from django.db import DatabaseError, transaction
from django.db.models import F

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from eduAcademy.views_checks import *
from courses.models import Lecture, Enrollment
from .serializers import *


####################
# Pay for lectures #
####################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def pay_for_lecture(request, lecture_id):
    if not request.user.is_authenticated:
        return Response({
                "detail": "User should be logged in to pay for a lecture",
                "redirect_to": reverse("api:login")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if not is_student(request.user):
        return Response({"detail": "User is not a student."}, status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(request.user):
        return Response({
                "detail": "Usrs's profile is not completed",
                "redirect_to": reverse("api:complete_profile"),
                "user_role": request.user.user_role.role
            },
            status=status.HTTP_403_FORBIDDEN
        )

    lecture = get_object_or_404(Lecture, pk=lecture_id)
    student = Student.objects.get(student=request.user)
    course = lecture.course
    teacher = course.teacher

    if request.method == "GET":
        return Response()

    serializer = PaymentsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data

    p = Payment(
        teacher=teacher,
        lecture=lecture,
        course=course,
        student=student,
    )
    
    if data['method'] == 'balance':
        if student.balance < course.lecture_price:
            return Response({"detail": "Insufficient balance"}, status=status.HTTP_403_FORBIDDEN)

        student_transaction = StudentBalanceTransaction(
            payment=p,
            student=student,
            amount=course.lecture_price,
        )
        student.balance = F('balance') - course.lecture_price
    elif data['method'] == 'points':
        if points_to_pounds(student.points) < course.lecture_price:
            return Response({"detail": "Insufficient points"}, status=status.HTTP_403_FORBIDDEN)

        student_transaction = PointsTransaction(
            payment=p,
            student=student,
            amount=pounds_to_points(course.lecture_price),
        )
        student.points = F('points') - pounds_to_points(course.lecture_price)
    
    try:
        with transaction.atomic():
            p.save()
            student.save()
            student_transaction.save()
    except IntegrityError:
        return Response({"detail": "You already bought this lecture before."}, status=status.HTTP_403_FORBIDDEN)
    except DatabaseError:
        return Response({"detail": "An error occured during the transaction."}, status=status.HTTP_400_BAD_REQUEST)

    if (Enrollment.objects.filter(student=student, course=course).count() == 0 and
    Payment.objects.filter(student=student, course=course).count() >= 2):
        Enrollment.objects.create(student=student, course=course)

    return Response({"detail": "Payment successful"})