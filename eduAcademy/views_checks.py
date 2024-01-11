from accounts.models import Teacher, Student, Assistant
from courses.models import Course
from payment_credits.models import Payment

roles_to_models = {"Teacher": Teacher, "Student": Student, "Assistant": Assistant}

def is_student(user):
    return Student.objects.filter(pk=user.pk).count()

def is_teacher(user):
    return Teacher.objects.filter(pk=user.pk).count()

def is_accepted_teacher(user):
    if is_teacher(user):
        return Teacher.objects.get(pk=user.pk).accepted
    return False

def is_assistant(user):
    return Assistant.objects.filter(pk=user.pk).count()

def profile_is_completed(user):
    return roles_to_models.get(user.user_role.role).objects.filter(pk=user.pk).count()

def student_enrolled_in_course(user, course_id:int):
    if is_student(user):
        student = Student.objects.get(student=user)
        course = student.course_set.filter(pk=course_id).count()
        return course
    return False

def teacher_created_course(user, course_id:int):
    if is_teacher(user):
        return Teacher.objects.get(teacher=user) == Course.objects.get(pk=course_id).teacher
    return False

def assistant_assisting_in_course(user, course_id:int):
    if is_assistant(user):
        assistant = Assistant.objects.get(assistant=user)
        course = assistant.course_set.filter(pk=course_id).count()
        return course
    return False

def student_bought_lecture(user, lecture):
    student = Student.objects.get(student=user)
    return Payment.objects.filter(student=student, lecture=lecture).count()

POINT_VALUE = 1/5
def points_to_pounds(points:int):
    return int(points * POINT_VALUE)
def pounds_to_points(pounds:int):
    return int(pounds / POINT_VALUE)