from rest_framework import serializers
from .models import Books,Order,Cart,WishList

'''This will serialize the complex data'''
class BookSerializer(serializers.ModelSerializer):
 class Meta:
  model = Books
  fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
 class Meta:
  model = Cart
  fields = ['book_id','quantity','price','total_amount']

class OrderSerializer(serializers.ModelSerializer):
 class Meta:
  model = Order
  fields = "__all__"

class WishListSerializer(serializers.ModelSerializer):
 class Meta:
  model = WishList
  fields = "__all__"