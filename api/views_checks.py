from .models import Teacher, Student, Assistant

roles_to_models = {"Teacher": Teacher, "Student": Student, "Assistant": Assistant}

def is_student(user):
    return len(Student.objects.filter(pk=user.pk)) == 1

def is_teacher(user):
    return len(Teacher.objects.filter(pk=user.pk)) == 1

def is_accepted_teacher(user):
    if is_teacher(user):
        return Teacher.objects.get(pk=user.pk).accepted
    return False

def is_assistant(user):
    return len(Assistant.objects.filter(pk=user.pk)) == 1

def profile_is_completed(user):
    return len(roles_to_models.get(user.user_role.role).objects.filter(pk=user.pk)) == 1