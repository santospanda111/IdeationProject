from django.db import models

class UserData(models.Model):
    """
    This represents the table of the database provided in the credentials. It provides the user details required
    for registration process to complete.
    """
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=100,null=True)