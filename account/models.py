from django.db import models

# Create your models here.
class Account(models.Model):
    aid = models.CharField(max_length=20,primary_key=True)
    pname = models.CharField(max_length=20)
    pid = models.CharField(max_length=30)
    tel = models.CharField(max_length=20, null=True)
    pbirth = models.DateField()
    psex = models.CharField(max_length=1)
    balance = models.FloatField()
    regtime = models.DateTimeField()
    logpwdhash = models.CharField(max_length=32) # sha256

    def __str__(self):
        return self.aid
    
class Record(models.Model):
    rid = models.CharField(max_length=20,primary_key=True)
    orig_id = models.CharField(max_length=20)
    recv_id = models.CharField(max_length=20)
    money = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return self.rid

class Cookie(models.Model):
    cookie = models.CharField(max_length=20,primary_key=True)
    uid = models.CharField(max_length=20)
    live = models.CharField(max_length=20)

    def __str__(self):
        return self.cookie