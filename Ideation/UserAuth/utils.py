import jwt
from django.conf import settings
from rest_framework.response import Response

def encode_token_userid(user_id):
    """
        This method is used to encode the token.
        :param request: It accepts userid as parameter.
        :return: It returns the encoded token.
    """
    try:
        encoded_token = jwt.encode({'user_id':user_id}, key=settings.SECRET_KEY, algorithm='HS256')
        return encoded_token
    except Exception as e:
        return Response({"message":str(e)})

def encode_token(user_id,user_name):
    """
        This method is used to encode the token.
        :param request: It accepts userid,username as parameter.
        :return: It returns the encoded token.
    """
    try:
        encoded_token_id = jwt.encode({'user_id':user_id,'username':user_name}, key=settings.SECRET_KEY, algorithm='HS256')
        return encoded_token_id
    except Exception as e:
        return Response({"message":str(e)})

def decode_token(encoded_token_id):
    """
        This method is used to decode the token.
        :param request: It accepts encoded token as parameter.
        :return: It returns the decoded token.
    """
    try:
        decoded_token = jwt.decode(encoded_token_id,key=settings.SECRET_KEY,algorithms="HS256")
        return decoded_token
    except Exception as e:
        return Response({"message":str(e)})