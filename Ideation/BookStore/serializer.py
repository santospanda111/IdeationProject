from rest_framework import serializers
from .models import Books,Order,Cart, OrderList,WishList

'''This will serialize the complex data'''
class BookSerializer(serializers.ModelSerializer):
 class Meta:
  model = Books
  fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
 class Meta:
  model = Cart
  fields = ['user_id','book_id','quantity']

class OrderSerializer(serializers.ModelSerializer):
 class Meta:
  model = Order
  fields = "__all__"

class WishListSerializer(serializers.ModelSerializer):
 class Meta:
  model = WishList
  fields = "__all__"

class OrderListSerializer(serializers.ModelSerializer):
 class Meta:
  model = OrderList
  fields = "__all__"