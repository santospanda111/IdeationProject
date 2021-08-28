from django.db import models
from UserAuth.models import UserData

class Books(models.Model):
    """
     Books Model : id, author, title, image, quantity, price, description
    """
    id = models.AutoField(primary_key=True,unique=True)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()

class Cart(models.Model):
    """
     Cart Model : user_id, book, quantity
    """
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    """
     Order Model : id, user_id, total_amount, is_delivered, ordered_date
    """
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    is_delivered = models.BooleanField(default=False,null=False)
    ordered_date = models.DateTimeField(auto_now_add=True)

class OrderList(models.Model):
    """
     OrderList Model : user_id, book
    """
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    
class WishList(models.Model):
    """
     WishList Model : id, user_id, book_id
    """
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)