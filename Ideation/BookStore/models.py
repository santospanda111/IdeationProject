from django.db import models
from UserAuth.models import UserData

class Books(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()

class Cart(models.Model):
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    is_delivered = models.BooleanField(default=False,null=False)
    ordered_date = models.DateTimeField(auto_now_add=True)

class WishList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)