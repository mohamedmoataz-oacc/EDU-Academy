from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from accounts.models import User, Teacher, Assistant


GATED_CONTENT = {
    # "gated path": (Model_to_query, attribute_to_search, attribute_containing_user_instance)
    "teachers/national_IDs/": (Teacher, 'national_ID_photo', 'teacher'),
    "assistants/national_IDs/": (Assistant, 'national_ID_photo', 'assistant'),
}

class GatedContent:
    """
    Prevents specific content directories from being exposed to non-authorized users
    """

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        new_resp = self.process_request(request)
        return new_resp or response
    
    def create_rendered_response(self, details: dict, status):
        response = Response(details, status=status)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response
    
    def is_authorized(self, file, location, user):
        data = GATED_CONTENT.get(location)
        if data is not None:
            record = data[0].objects.filter(**{data[1]: location + file})
            if record.exists():
                data_user = getattr(record[0], data[2])
                return user.username == data_user.username
        return True

    def process_request(self, request):
        user = request.user
        path = request.path
        while path.endswith('/') or path.endswith('.'):
            path = path[:-1]

        authorized = True
        is_gated = path.startswith("/media/")
        if is_gated:
            file = path.split("/")[-1]
            location = '/'.join(path.split("/")[2:-1]) + '/'
            authorized = self.is_authorized(file, location, user)
        
        if not authorized:
            return self.create_rendered_response(
                details={"detail":"You are not authorized to access this file."},
                status=status.HTTP_401_UNAUTHORIZED
            )