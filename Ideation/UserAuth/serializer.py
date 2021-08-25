from rest_framework import serializers
from .models import UserData

'''This will serialize the complex data'''
class UserSerializer(serializers.ModelSerializer):
 class Meta:
  model = UserData
  fields = "__all__"