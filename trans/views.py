from django.shortcuts import render
from account.models import *
from django.http import *
from hashlib import sha256,sha1
import secrets
import time
from gmssl import  sm2,sm3,sm4,func
from Crypto.Util.number import *
from gmpy2 import *
import base64
import Crypto.Cipher.DES
from trans.config import bankpubkey_n,bankpubkey_d,bankpubkey_e,Cer_e,Cer_n
from datetime import datetime

# Create your views here.

def deal(request):
    if request.method != "POST":
        return HttpResponse("Error!")
    try:
        Sign = int(request.POST.get('Sign'))
        PI = request.POST.get('PI')
        H_OI = int(request.POST.get('H_OI'))
        User_e = int(request.POST.get('User_e'))
        User_n = int(request.POST.get('User_n'))
        Cer = request.POST.get('Cer')
        payer = request.POST.get('payer')
    except:
        return HttpResponse("Error!")
    # 提取PI
    PI = int(PI)
    PI = powmod(PI,bankpubkey_d,bankpubkey_n)
    PI = long_to_bytes(PI)
    H_PI = sm3.sm3_hash(func.bytes_to_list(PI))

    PI = PI.split(b':')
    payee = PI[0].decode()
    price = int(PI[1])
    u_time = PI[2].decode()
    cardnumber = PI[3].decode()
    # 校验证书
    Cer = int(Cer,16)
    Cer = powmod(Cer,Cer_e,Cer_n)
    Cer = long_to_bytes(Cer)
    Cer_msg = b''
    Cer_msg += str(User_e).encode() + b':'
    Cer_msg += str(User_n).encode() + b':'
    Cer_msg += payer.encode() + b':RSA'
    Cer_msg = sm3.sm3_hash(func.bytes_to_list(Cer_msg))
    if Cer != Cer_msg.encode():
        return HttpResponse('证书错误!')
    
    # 校验双重签名
    H_OI = powmod(H_OI,bankpubkey_d,bankpubkey_n)
    H_OI = long_to_bytes(H_OI)
    Sign = powmod(Sign,User_e,User_n)
    Sign = long_to_bytes(Sign)
    Sign2 = sm3.sm3_hash(func.bytes_to_list(H_OI+H_PI.encode()))
    if Sign != Sign2.encode():
        return HttpResponse('双重签名校验失败!')   

    # 校验时间戳
    if time.time()-int(u_time) > 3600:
        return HttpResponse("签名过期") 

    # 校验用户有无钱钱
    user = Account.objects.filter(aid=cardnumber)
    if not len(user):
        return HttpResponse("用户不存在") 
    balance = user.values()[0]['balance']
    #print(balance,price)
    if price > balance:
        return HttpResponse("余额不足")
    print(payee)
    recv = Account.objects.filter(aid=payee)
    print(recv)
    recv = recv[0]
    recv.balance = recv.balance + price
    recv.save()

    user = user[0]
    user.balance = user.balance - price
    user.save()
    
    insert_record(cardnumber, payee, price)
    return HttpResponse('OK')


def insert_record(orig, recv, money):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    record = Record(rid=sha1(str(time.time()).encode()).hexdigest(), orig_id=orig, recv_id=recv, money=money, time=formatted_time)
    record.save()