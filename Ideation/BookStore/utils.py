from django.http import JsonResponse
import jwt
from django.conf import settings
from log import get_logger

# Logger configuration
logger = get_logger()

def verify_token(function):
    '''This method will verify the token'''
    def wrapper(self, request):
        token = request.headers.get('Authorization') or request.META.get('HTTP_TOKEN')
        if not token:
            resp = JsonResponse({'message': 'Token not provided in the header'})
            resp.status_code = 400
            logger.info('Token not provided in the header')
            return resp
        user_details= jwt.decode(token,key=settings.SECRET_KEY,algorithms="HS256")
        user_id= user_details.get('user_id')
        request.data.update({"id":user_id})
        return function(self, request) 
    return wrapper