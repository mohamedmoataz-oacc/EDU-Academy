from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from accounts.models import User, Teacher, Assistant


GATED_CONTENT = {
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

    # TODO: refactor this code
    def process_request(self, request):
        path = request.path
        while path.endswith('/') or path.endswith('.'):
            path = path[:-1]
        user = request.user

        is_gated = path.startswith("/media/")
        not_authorized = False
        if is_gated:
            file = path.split("/")[-1]
            location = '/'.join(path.split("/")[2:-1]) + '/'

            data = GATED_CONTENT.get(location)
            if data is not None:
                record = data[0].objects.filter(**{data[1]: location + file})
                if record.exists():
                    data_user = getattr(record[0], data[2])
                    if user.username != data_user.username: not_authorized = True
        
        if not_authorized:
            response = Response(
                {"detail":"You are not authorized to access this file."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response