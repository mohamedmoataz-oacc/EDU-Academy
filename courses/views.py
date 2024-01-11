from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .roles_actions import roles_to_actions, get_basic_course_info
from eduAcademy.views_checks import *
from .serializers import *


#################
# Create course #
#################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def create_course(request):
    if not request.user.is_authenticated:
        return Response({
                "detail":" The user is not authenticated to create a course",
                "redirect_to": reverse("api:login")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if not profile_is_completed(request.user):
        return Response({
                "detail":"User should complete his profile",
                "redirect_to": reverse("api:complete_profile"),
                "user_role": request.user.user_role.role
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not is_accepted_teacher(request.user):
        return Response({"detail": "The teacher request either is still not reviwed or was rejected"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        return Response()
    elif request.method == 'POST':
        data = {**request.data, **request.FILES}
        data = {i:j[0] if isinstance(j, list) else j for i, j in data.items()}

        serializer = CourseCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data['subject'] = serializer.data['subject']

        Course.objects.create(
            teacher = Teacher.objects.get(teacher=request.user),
            subject = Subject.objects.get(pk=data['subject']),
            course_name = data['course_name'],
            description = data['description'],
            lecture_price = data['lecture_price'],
            package_size = data['package_size'],
            thumbnail = data['thumbnail']
        )
        return Response({"detail": "The course has been created successfully"})

###############
# View Course #
###############

@api_view(['GET'])
def view_course(request, course_id:int):
    user = request.user
    if user.is_authenticated:
        return Response(roles_to_actions[user.user_role.role]["view_course"](user, course_id))
    else:
        return Response(get_basic_course_info(course_id)[0])

##################
# Create lecture #
##################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def create_lecture(request, course_id:int = None):
    if not request.user.is_authenticated:
        return Response({
                "detail":"The user is not authenticated to create a lecture",
                "redirect_to": reverse("api:login")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if not is_accepted_teacher(request.user):
        return Response({"detail": "User should be a teacher to create a lecture"},
                        status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(request.user):
        return Response({
                "detail":"User should complete his profile to create a lecture",
                "redirect_to": reverse("api:complete_profile"),
                "user_role": request.user.user_role.role
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    course = Course.objects.filter(teacher=Teacher.objects.get(teacher=request.user), pk=course_id)
    if not course.count():
        return Response({"detail": "Teacher is trying to create a lecture in other teacher course or an inexistent course"},
                        status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        data = {**request.data, **request.FILES}
        data = {i:j[0] if isinstance(j, list) else j for i, j in data.items()}

        serializer = LectureCreationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        Lecture.objects.create(
            course = course[0],
            lecture_title = data['lecture_title'],
            video = data['video'],
        )
        return Response({
                "detail":"Lecture created successfully",
                "redirect_to": reverse("api:view_lecture", args=(course[0].pk, data['lecture_title']))
            }
        )
    elif request.method == 'GET': return Response()
    

################
# View Lecture #
################

@api_view(['GET'])
def view_lecture(request, course_id:int, lecture_slug:str):
    user = request.user
    if not user.is_authenticated:
        return Response({
                "detail":"User should be logged in to view lecture",
                "redirect_to": reverse("api:login")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    course = Course.objects.get(pk=course_id)
    lecture = get_object_or_404(Lecture, lecture_slug=lecture_slug, course=course)
    return roles_to_actions[user.user_role.role]["view_lecture"](user, lecture)


##############
# My courses #
##############

@api_view(['GET'])
def my_courses(request):
    user = request.user
    if not request.user.is_authenticated:
        return Response({
                "detail":"User should be logged in to view his courses",
                "redirect_to": reverse("api:login")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if not profile_is_completed(user):
        return Response({
                "detail":"User should complete his profile to view his courses",
                "redirect_to": reverse("api:complete_profile"),
                "user_role": request.user.user_role.role
            },
            status=status.HTTP_403_FORBIDDEN
        )
    return Response(roles_to_actions[user.user_role.role]["my_courses"](user))


###############
# Get courses #
###############

@api_view(['GET'])
def get_courses(request, subset=None):
    if not subset: return Response({"redirect_to":reverse("api:get_portion_courses", args=(1,))})
    fields_to_filters = {
        "subject": "subject__subject_name",
        "teacher": "teacher__teacher__full_name__icontains",
        "completed": "completed",
    }
    fields = request.GET
    filters = dict()
    for i, j in fields.items():
        if i not in fields_to_filters: continue
        filters[fields_to_filters[i]] = j
    
    all_courses = Course.objects.all()
    all_courses = all_courses.filter(**filters)[20*(subset-1):20*subset]
    
    filtered_courses = [
        {
            "id": course.id,
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            "thumbnail": f"media/{course.thumbnail}",
            "subject": course.subject.subject_name,
        } for course in all_courses
    ]
    return Response(filtered_courses)


################
# Get subjects #
################

@api_view(['GET'])
def get_subjects(request):
    subjects =  {"Subjects": Subject.objects.all()}
    return Response(subjects)


##################
# Courses search #
##################

@api_view(['GET'])
def search_course(request, name):
    courses_matched = Course.objects.filter(course_name__icontains=name)
    courses = [
        {
            "id": course.id,
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            "thumbnail": f"media/{course.thumbnail}",
            "subject": course.subject.subject_name,
        } for course in courses_matched
    ]
    return Response(courses)

