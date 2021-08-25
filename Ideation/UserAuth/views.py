from rest_framework.views import APIView,Response,status
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from UserAuth.utils import encode_token,decode_token,encode_token_userid
from django.db.models import Q

class Index(APIView):

    def get(self,request):
        """
        [This method will return welcome message]

        """
        return Response({'message':'Welcome to Ideation Project'})

class Register(APIView):
    
    def get(self,request,pk=None):
        """
            This method is used to read the data from user_data.
            :param request: It accepts pk(primary_key) as parameter.
            :return: It returns the registered data.
        """
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


    def post(self,request):
        """
            This method is used to register new user.
            :param request: It accepts first_name, last_name, email, username and password as parameter.
            :return: It returns the message if successfully registered.
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if User.objects.filter(username=serializer.data.get('username')).exists():
                return Response({'message': 'Username is already registered with another user.'}, status=status.HTTP_400_BAD_REQUEST)
            # Register user
            user = User.objects.create_user(first_name=serializer.data.get('first_name'), last_name=serializer.data.get('last_name'), email=serializer.data.get('email'), username=serializer.data.get('username'), password=serializer.data.get('password'))
            # Save user
            user.save()
            user_name=serializer.data.get('username')
            user_id= User.objects.get(username=user_name).id
            print(user_id)
            token = encode_token(user_id,user_name)
            email= serializer.data.get("email")
            subject, from_email, to='Register yourself by complete this verification','santospanda111@gmail.com',email
            html_content= f'<a href="http://127.0.0.1:8000/verify/{token}">Click here</a>'
            text_content='Verify yourself'
            msg=EmailMultiAlternatives(subject,text_content,from_email,[to])
            msg.attach_alternative(html_content,"text/html")
            msg.send()
            return Response({"message":"CHECK EMAIL for verification"})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
   
    def post(self,request):
        """
            This method is used for login authentication.
            :param request: It's accept username and password as parameter.
            :return: It returns the message if successfully loggedin.
        """
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            id = User.objects.get(username=username).id
            token=encode_token_userid(id)           
            if user is None:
                return Response({"msg": 'Wrong username or password'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "Loggedin Successfully", 'data' : {'username': username,'token': token}}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': "wrong credentials"}, status=status.HTTP_400_BAD_REQUEST) 
        except AuthenticationFailed:
            return Response({'message': 'Authentication Failed'}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            return Response({"msg": "wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):

    def get(self,request,token=None):
        """
            This method is used to verify the email_id.
            :param request: It's accept token as parameter.
            :return: It returns the message if Email successfully verified.
        """
        try:
            user= decode_token(token)
            user_id=user.get("user_id")
            username=user.get("username")
            if User.objects.filter(Q(id=user_id) & Q(username=username)):
                return Response({"message":"Email Verified and Registered successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Try Again......Wrong credentials"})
        except Exception as e:
            return Response({"message":str(e)})