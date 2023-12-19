"""
Contains functions for the actions that are different between user roles.
"""

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .views_checks import *
from .models import *

# Note that `request.FILES` will only contain data if the request method was POST,
# at least one file field was actually posted,
# and the <form> that posted the request has the attribute enctype="multipart/form-data".
# Otherwise, `request.FILES` will be empty.


######################
# Profile completion #
######################

def teacher_complete_profile(request):
    serializer = TeacherProfileSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
    
    teacher = Teacher.objects.create(
        teacher = request.user,
        personal_photo = data['personal_photo'],
        national_ID_photo = data['national_ID_photo'],
    )
    teacher.save()
    TeachRequest.objects.create(teacher=teacher).save()
    return Response({"user_role":request.user.user_role.role, "redirect_to":reverse("api:view_profile", args=(request.user.username,))})

def student_complete_profile(request):
    serializer = StudentProfileSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
    
    Student.objects.create(
        student=request.user,
        academic_year = data['academic_year'],
        study_field = data['study_field'] if data.get('study_field') else None,
        parent_name = data['parent_name'],
        parent_phone_number = data['parent_phone_number'],
        personal_photo = data['personal_photo'] if data.get('personal_photo') else None,
    ).save()
    return Response({"user_role":request.user.user_role.role, "redirect_to":reverse("api:view_profile", args=(request.user.username,))})

def assistant_complete_profile(request):
    serializer = AssistantProfileSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
    
    Assistant.objects.create(
        assistant=request.user,
        personal_photo = data['personal_photo'],
        national_ID_photo = data['national_ID_photo'],
    ).save()
    return Response({"user_role":request.user.user_role.role, "redirect_to":reverse("api:view_profile", args=(request.user.username,))})


###################
# Profile viewing #
###################

def teacher_view_profile(user, user_profile: dict, view_self):
    teacher = Teacher.objects.get(teacher=user)
    user_profile.update(
        {
            "balance" : teacher.balance if view_self else None,
            "accepted" : teacher.accepted,
            "personal_photo" : f"media/{teacher.personal_photo}",
            "national_ID_photo" : f"media/{teacher.national_ID_photo}" if view_self else None,
        }
    )
    return Response(user_profile)
    
def student_view_profile(user, user_profile: dict, view_self):
    student = Student.objects.get(student=user)
    badges_list = student.badge_set.all()
    user_profile.update(
        {
            "academic_year" : student.academic_year,
            "study_field" : student.study_field,
            "parent_phone_number" : student.parent_phone_number,
            "parent_name" : student.parent_name,
            "points" : student.points if view_self else None,
            "balance" : student.balance if view_self else None,
            "verified" : student.verified if view_self else None,
            "personal_photo" : f"media/{student.personal_photo}" if student.personal_photo else None,
            "badges" : [badge.badge_name for badge in badges_list]
        }
    )
    return Response(user_profile)

def assistant_view_profile(user, user_profile: dict, view_self):
    assistant = Assistant.objects.get(assistant=user)
    user_profile.update(
        {
            "personal_photo" : f"media/{assistant.personal_photo}",
            "national_ID_photo" : f"media/{assistant.national_ID_photo}" if view_self else None,
        }
    )
    return Response(user_profile)


########
# Home #
########

# def teacher_home(user):
#     return Response("Home Page")

# def student_home(user):
#     enrolled_courses = student_my_courses(user)
#     student = Student.objects.get(student=user)
#     courses = Course.objects.all().difference(student.course_set.all())[:20]

#     not_enrolled_courses = [
#         {
#             "name": course.course_name,
#             "description": course.description,
#             "is_completed": course.completed,
#             "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
#                        User.objects.get(pk=course.teacher.pk).last_name,
#             "thumbnail" : f"media/{course.thumbnail}",
#             "subject": course.subject.subject_name,
#         } for course in courses
#     ]

#     output = {
#         "enrolled_courses": enrolled_courses,
#         "not_enrolled_courses": not_enrolled_courses,
#     }

#     return Response(output)

# def assistant_home(user):
#     return Response("Home Page")


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
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return get_lecture_content(lecture)

def student_view_lecture(user, lecture):
    if not student_bought_lecture(user, lecture):
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    return get_lecture_content(lecture)

def assistant_view_lecture(user, lecture):
    if not assistant_assisting_in_course(user, lecture.course.pk):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return get_lecture_content(lecture)

####################
# Roles -> actions #
####################

roles_to_actions = {
    "Teacher": {
        "completion": teacher_complete_profile,
        "viewing": teacher_view_profile,
        # "home": teacher_home,
        "my_courses": teacher_my_courses,
        "view_course": teacher_view_course,
        "view_lecture": teacher_view_lecture,
    },
    "Student": {
        "completion": student_complete_profile,
        "viewing": student_view_profile,
        # "home": student_home,
        "my_courses": student_my_courses,
        "view_course": student_view_course,
        "view_lecture": student_view_lecture,
    },
    "Assistant": {
        "completion": assistant_complete_profile,
        "viewing": assistant_view_profile,
        # "home": assistant_home,
        "my_courses": assistant_my_courses,
        "view_course": assistant_view_course,
        "view_lecture": assistant_view_lecture,
    },
}