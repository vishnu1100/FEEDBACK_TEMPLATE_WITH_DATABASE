from django.db import models

class login(models.Model):
    logid = models.AutoField(primary_key=True)
    username = models.CharField("username",max_length=100)
    password =  models.CharField("password",max_length=100)
    role=models.CharField('role',max_length=10)

class Feedback(models.Model):
    feed_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    message = models.TextField()
    status=models.CharField(max_length=20)
    date_time = models.DateTimeField(auto_now_add=True)
    reply=models.CharField("reply",max_length=100,null=True)
    staff=models.CharField("staff",max_length=30,null=True)

    def __str__(self):
        return self.name


# Create your models here.
