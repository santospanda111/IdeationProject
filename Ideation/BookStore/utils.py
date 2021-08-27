from logging import Logger
from django.http import JsonResponse
import jwt
from django.conf import settings


def verify_token(function):
    '''This method will verify the token'''
    def wrapper(self, request):
        
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = JsonResponse({'message': 'Token not provided in the header'})
            resp.status_code = 400
            Logger.info('Token not provided in the header')
            return resp
        user_details= jwt.decode(request.META.get('HTTP_AUTHORIZATION'),key=settings.SECRET_KEY,algorithms="HS256")
        user_id= user_details.get('user_id')
        request.data.update({"id":user_id})
        return function(self, request) 
    return wrapper