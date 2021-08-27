from rest_framework.views import APIView,Response,status
from .serializer import BookSerializer
from UserAuth.models import UserData
from .models import Books
from .utils import verify_token
from rest_framework.exceptions import ValidationError

class AddBooks(APIView):

    @verify_token
    def post(self,request):
        """
        This method adds the book details to the database. This can only be done by admin
        :return: adds the book details to the database
        """
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            if user.status == 'admin':
                serializer = BookSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                book = Books(author=request.data['author'],title=request.data['title'],image=request.data['image'],
                            quantity=request.data['quantity'],price=request.data['price'],description=request.data['description'])
                book.save()
                return Response({'message':'Book Created Successfully'},status=status.HTTP_200_OK)
            return Response({'message':'Sorry, Only Admin can add books.'},status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetBooks(APIView):

    def get(self,request):
        """
        This method queries all the book details in Books database
        :return: book details in database.
        """
        try:
            data = Books.objects.all()
            serializer = BookSerializer(data, many=True)
            return Response({'Data':serializer.data})
        except ValidationError:
            return Response({'message': 'Invalid serializer'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
