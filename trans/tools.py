from django.shortcuts import render
from account.models import *
from django.http import *
from hashlib import sha256
import secrets
import time
from Crypto.Util.number import *

def Cer_decode(cer):
    pass

def read_cer(aid):
    user = Account.objects.filter(aid=aid)
    if not len(user):
        return None
    pos = 'E:\\work\\ebank\\cert\\'+user.values()[0]['cert']
    cer = open(pos,"rb").read()
    return cer

def self_cer():
    return open("E:\\work\\ebank\\cert\\local.cer","rb").read()

def Sign_decode(sign):
    pass