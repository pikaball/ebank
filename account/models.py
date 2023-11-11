from django.db import models

# Create your models here.
class Account(models.Model):
    aid = models.CharField(max_length=20,primary_key=True)
    pname = models.CharField(max_length=20)
    pid = models.CharField(max_length=30)
    pbirth = models.DateField()
    psex = models.CharField(max_length=1)
    pcountry = models.CharField(max_length=20)
    balance = models.IntegerField()
    regtime = models.DateTimeField()
    cert = models.CharField(max_length=50)
    logpwdhash = models.CharField(max_length=32) # sha256

    def __str__(self):
        return self.aid
    
class Record(models.Model):
    rid = models.CharField(max_length=20,primary_key=True)
    orig_id = models.CharField(max_length=20)
    recv_id = models.CharField(max_length=20)
    money = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.rid

class Cookie(models.Model):
    cookie = models.CharField(max_length=20,primary_key=True)
    uid = models.CharField(max_length=20)
    live = models.DateTimeField()

    def __str__(self):
        return self.cookie