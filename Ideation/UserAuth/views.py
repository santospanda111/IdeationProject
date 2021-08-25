from rest_framework.views import APIView,Response,status
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework.exceptions import ValidationError

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
            return Response({'message':'Registration Successful'},status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)