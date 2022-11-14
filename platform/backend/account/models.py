from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class mlangles_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class mlangles_user_details(models.Model):
    username = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    org = models.CharField(max_length=100)
    org_mail = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    pass_one = models.CharField(max_length=100)