from rest_framework.serializers import Serializer
from rest_framework.views import APIView,Response,status
from .serializer import BookSerializer,CartSerializer
from UserAuth.models import UserData
from .models import Books,Cart
from .utils import verify_token

class AddBooks(APIView):

    @verify_token
    def post(self,request):
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
        except Exception as e:
            return Response({'message': str(e)})

class GetBooks(APIView):

    def get(self,request):
        try:
            data = Books.objects.all()
            serializer = BookSerializer(data, many=True)
            return Response({'Data':serializer.data})
        except Exception as e:
            return Response({'message': str(e)})

class AddToCart(APIView):
    @verify_token
    def get(self,request):
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            totalitem = len(Cart.objects.filter(user_id=user))
            print(totalitem)
            cart = Cart.objects.filter(user_id=user)
            amount = 0
            totalamount=0
            print(cart)
            for item in cart:
                print(item.book_id)
                book = Books.objects.filter(id=item.book_id)
                print(book)
                tempamount = (item.quantity * book)
                amount += tempamount
                totalamount = amount
                print(totalamount)
            print(book)
            return Response("Hello")
        except Exception as e:
            return Response({"message":str(e)})


    @verify_token
    def post(self,request):
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            book_id= request.data['book_id']
            book_title = Books.objects.get(id=book_id)
            cart_item = Cart(user_id=user, book=book_title,quantity=request.data['quantity'])
            cart_item.save()
            return Response({'message':'Added to cart successfully'})
        except Exception as e:
            return Response({'message':str(e)})