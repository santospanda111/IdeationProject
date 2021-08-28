from rest_framework.views import APIView,Response,status
from .serializer import BookSerializer,CartSerializer,OrderListSerializer
from UserAuth.models import UserData
from .models import Books,Cart,Order,OrderList
from .utils import verify_token
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

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

class AddToCart(APIView):
    
    @verify_token
    def get(self,request):
        """
        This method requires user_id to get cart information with total amount.
        :param user_id: payload in the jwt.
        :return: items in cart with total amount.
        """
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            data = Cart.objects.filter(user_id=user)
            serializer = CartSerializer(data, many=True)
            amount = 0
            totalamount=0
            for item in data:
                book = Books.objects.filter(id=item.book_id).first()
                tempamount = (item.quantity * book.price)
                amount += tempamount
                totalamount = amount
            return Response({"data":serializer.data,"total_amount":totalamount})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


    @verify_token
    def post(self,request):
        """
        This method requires book id to add to the cart one by one contains book id, quantity
        :param user_id: payload in the jwt, book_id, quantity
        :return: response whether items added to cart or not.
        """
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            book_id= request.data['book_id']
            book = Books.objects.get(id=book_id)
            if book.quantity>0:
                book.quantity -= request.data['quantity']
                book.save()
                cart_item = Cart(user_id=user, book=book,quantity=request.data['quantity'])
                cart_item.save()
                return Response({'message':'Added to cart successfully'})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

class SearchBook(APIView):

    def get(self, request):
        """
        This method requires data to search book from book store.
        :param : title or author or id
        :return: book data according to the title or author or id.
        """
        try:
            book = Books.objects.filter(Q(title=request.data['keyword']) | Q(author=request.data['keyword']) | Q(id=request.data['keyword'])).all()
            serializer = BookSerializer(book, many=True)
            return Response({"data": serializer.data})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class OrderPlace(APIView):
    
    @verify_token
    def get(self, request):
        """
        This method requires user_id to get the order_list
        :param user_id: payload in the jwt.
        :return: the order list
        """
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            orders= OrderList.objects.filter(user_id=user)
            serializer = OrderListSerializer(orders, many=True)
            return Response({"Order_List":serializer.data})
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def post(self,request):
        """
        This method requires user_id to place the order from the cart.
        Added confirmation mail.
        :param user_id: payload in the jwt.
        :return: response whether order placed successfully or not.
        """
        try:
            user = UserData.objects.filter(id = request.data.get("id")).first()
            data = Cart.objects.filter(user_id=user)
            cart_serializer = CartSerializer(data, many=True)
            amount = 0
            totalamount=0
            for item in data:
                book = Books.objects.filter(id=item.book_id).first()
                tempamount = (item.quantity * book.price)
                amount += tempamount
                totalamount = amount
                order_list = OrderList(user_id=user, book=book)
                order_list.save()
                item.delete()
            order = Order(user_id=user,total_amount=totalamount)
            order.save()

            subject = 'welcome to Book-Store'
            message = """
            Subject: Book order details
            Hi %s
            Order Confirmed
            Your total amount for the 
            books ordered is Rs.%d
            """ % (user.username, totalamount)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return Response({"message":"Order Placed Successfully","order_id":order.id,"total_amount":totalamount,"data":cart_serializer.data})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Order Unsuccessful"},status=status.HTTP_400_BAD_REQUEST)
