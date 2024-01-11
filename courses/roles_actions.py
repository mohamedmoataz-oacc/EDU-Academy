"""
Contains functions for the actions that are different between user roles.
"""

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from eduAcademy.views_checks import *
from .models import *



##############
# My courses #
##############

def teacher_my_courses(user):
    teacher = Teacher.objects.get(teacher=user)
    courses = teacher.course_set.all()
    output = [
        {
            "course_id": course.id,
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "creation_date": course.creation_date.date(),
            "thumbnail" : f"media/{course.thumbnail}",
            "subject": course.subject.subject_name,
        } for course in courses
    ]
    output = {
        "user_role": "Teacher",
        "courses" : output,
    }
    return output

def student_my_courses(user):
    student = Student.objects.get(student=user)
    courses = student.course_set.all()
    output = [
        {
            "course_id": course.id,
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "enrolled_date": Enrollment.objects.get(course=course, student=student).start_date.date(),
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            "thumbnail" : f"media/{course.thumbnail}",
            "subject": course.subject.subject_name,
        } for course in courses
    ]
    output = {
        "user_role": "Student",
        "courses" : output,
    }
    return output

def assistant_my_courses(user):
    assistant = Assistant.objects.get(assistant=user)
    courses = assistant.course_set.all()
    output = [
        {
            "course_id": course.id,
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "assisting_date": Assisting.objects.get(course=course, assistant=assistant).start_date.date(),
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            "thumbnail" : f"media/{course.thumbnail}",
            "subject": course.subject.subject_name,
        } for course in courses
    ]
    output = {
        "user_role": "Student",
        "courses" : output,
    }
    return output

###############
# View course #
###############

def get_basic_course_info(course_id:int):
    course = get_object_or_404(Course, pk=course_id)
    info = {
        "course_id": course.id,
        "course_name" : course.course_name,
        "teacher" : {
            f"{course.teacher.teacher.first_name} {course.teacher.teacher.last_name}" : 
                reverse("api:view_profile",args=(course.teacher.teacher.username,))
        },
        "subject" : course.subject.subject_name,
        "lectures" : [
            {
                "lecture_title" : lecture.lecture_title,
                "lecture_slug" : lecture.lecture_slug,
                "upload_date" : lecture.upload_date
            } for lecture in Lecture.objects.filter(course=course)
        ],
        "assistants" : [
            {
                f"{assistant.assistant.first_name} {assistant.assistant.last_name}" :
                    reverse("api:view_profile",args=(assistant.assistant.username,))
            } for assistant in course.assistants.all()
        ],
        "description" : course.description,
        "lecture_price" : course.lecture_price,
        "package_size" : course.package_size,
        "thumbnail" : f"media/{course.thumbnail}",
        "creation_date" : course.creation_date,
        "completed" : course.completed,
        "rating" : CourseRating.objects.filter(course=course).aggregate(avg_rating=Avg('rating'))['avg_rating']
    }
    return (info, course)

def teacher_view_course(user, course_id):
    basic_course_info, course = get_basic_course_info(course_id)
    if not teacher_created_course(user, course_id):
        return basic_course_info
    
    basic_course_info.update(
        {
            "students" : [
                {
                    f"{student.student.first_name} {student.student.last_name}" :
                        reverse("api:view_profile",args=(student.student.username,))
                } for student in course.students.all()
            ]
        }
    )
    output = {"user_role": "Teacher", "course_info": basic_course_info}
    return output

def student_view_course(user, course_id):
    student = Student.objects.get(student=user)
    basic_course_info, course = get_basic_course_info(course_id)    
    if not student_enrolled_in_course(user, course_id):
        return basic_course_info
    basic_course_info.update(
        {
            "enrollment_date" :  Enrollment.objects.get(student=student, course=course).start_date,
            "warnings_count" : Warnings.objects.filter(student=student, course=course).count()
        }
    )
    output = {"user_role": "Student", "course_info": basic_course_info}
    return output

def assistant_view_course(user, course_id):
    assistant = Assistant.objects.get(assistant=user)
    basic_course_info, course = get_basic_course_info(course_id)    
    if not assistant_assisting_in_course(user, course_id):
        return basic_course_info
    basic_course_info.update(
        {
            "start_date" :  Assisting.objects.get(assistant=assistant, course=course).start_date,
        }
    )
    output = {"user_role": "Assistant", "course_info": basic_course_info}
    return output

#######################
# Get lecture content #
#######################

def get_lecture_content(lecture):
    attachments_number = Attachment.objects.filter(lecture=lecture).count()
    quiz = Quiz.objects.filter(lecture=lecture)
    assignment = Assignment.objects.filter(lecture=lecture)
    qa = QA.objects.filter(lecture=lecture)
    content = {
        "lecture_id": lecture.id,
        "attached_files_number" : attachments_number,
        "video": f"media/{lecture.video}",
        "Quiz" : {
            "quiz_id" : quiz[0].id,
            "quiz_duration_in_minutes" : quiz[0].duration_in_minutes,
            "start_date" : quiz[0].start_date
        } if len(quiz) else None,
        "assignment" : {
            "assignment_id" : assignment[0].id,
            "assignment_upload_date" : assignment[0].upload_date 
        } if len(assignment) else None,
        "QA" : [
            {
                "qa_id" : q.pk,
                "qa_student_username" : q.student.student.username,
                "qa_question" : q.question,
                "closed" : q.closed,
                "qa_date" : q.question_date,
                "answers" : [
                    {
                        "qa_answer_student" : answer.user.username,
                        "upvotes_number" : answer.upvotes,
                        "marked_as_correct" : answer.marked_correct,
                        "answer_date" : answer.answer_date,
                    } for answer in QAAnswer.objects.filter(qa=q, lecture=lecture)
                ]
            } for q in qa
        ] if len(qa) else None,
    }
    return content

################
# View lecture #
################

def teacher_view_lecture(user, lecture):
    if not teacher_created_course(user, lecture.course.pk):
        return Response({
                "detail": "Teacher must own the course to be able to view its lectures."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(get_lecture_content(lecture))

def student_view_lecture(user, lecture):
    if not student_bought_lecture(user, lecture):
        return Response({
                "detail": "Student must buy the lecture to be able to view it."
            },
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    return Response(get_lecture_content(lecture))

def assistant_view_lecture(user, lecture):
    if not assistant_assisting_in_course(user, lecture.course.pk):
        return Response({
                "detail": "Assistant must be assisting in course to be able to view its lectures."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(get_lecture_content(lecture))

####################
# Roles -> actions #
####################

roles_to_actions = {
    "Teacher": {
        "my_courses": teacher_my_courses,
        "view_course": teacher_view_course,
        "view_lecture": teacher_view_lecture,
    },
    "Student": {
        "my_courses": student_my_courses,
        "view_course": student_view_course,
        "view_lecture": student_view_lecture,
    },
    "Assistant": {
        "my_courses": assistant_my_courses,
        "view_course": assistant_view_course,
        "view_lecture": assistant_view_lecture,
    },
}