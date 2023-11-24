from django.shortcuts import render
from account.models import Account,Cookie
from django.http import *
from hashlib import sha256
import secrets
import time

# Create your views here.
def home(requests):
    context = {
        'username' : 'test',
        'token' : None
    }
    try:
        context['token'] = requests.COOKIES['token']
    except:
        pass
    return render(requests,'home.html',context)

def login(requests):
    if requests.method == 'POST':
        tel = requests.POST['tel']
        pwd = requests.POST['pwd']
        context = {'fall':'yes','message':'信息不完整'}
        if tel and pwd:
            user = Account.objects.filter(tel=tel)
            print(user)
            if not len(user):
                context['message'] = '用户不存在'
            elif sha256(pwd.encode()).digest().hex() == user.values()[0]['logpwdhash']:
                response = HttpResponse('success')
                token = secrets.token_hex(32)
                response.set_cookie('token', token)
                coo = Cookie(cookie=token, uid=user.values()[0]['aid'], live=str(time.time()+3600))
                coo.save()
                return response
            else:
                context['message'] = '密码错误'
                
        print(context)
        return render(requests, 'login.html', context)
    return render(requests, 'login.html',{'message':'test'})