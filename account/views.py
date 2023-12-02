from django.shortcuts import render
from account.models import *
from django.http import *
from hashlib import sha256
import secrets
import time
from datetime import datetime

# Create your views here.
def home(requests):
    token = requests.COOKIES['token']
    context = getinfo(token)
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
        return HttpResponse(context['message'])
        # return render(requests, 'login.html', context)
    return render(requests, 'login.html',{'message':'test'})

def vistr(value, length):
    return 0 < len(value) <= length and not any(char in value for char in [' ', "'","\""])

def vinum(value, length):
    return 0 < len(value) <= length and value.isdigit()

def check_input(aid, pname, pid, psex, tel, pwd):
    def err(message):
        return message

    if not vinum(aid, 20):
        return err("不合法的卡号")
    elif not vistr(pname, 20):
        return err("不合法的姓名")
    elif not (vinum(pid, 18) and len(pid) == 18):
        return err("不合法的证件号")
    elif psex.lower() not in ['m', 'f']:
        return err("请输入正确性别")
    elif not (vinum(tel, 11) and len(tel) == 11):
        return err("不合法的手机号")
    elif not vistr(pwd, 20):
        return err("不合法的密码")
    else:
        return None

def register(requests):
    if requests.method == 'POST':
        aid = requests.POST['aid']
        pname = requests.POST['pname']
        pid = requests.POST['pid']
        pbirth = requests.POST['pbirth']
        psex = requests.POST['psex']
        tel = requests.POST['tel']
        pwd = requests.POST['pwd']
        check = check_input(aid,pname,pid,psex,tel,pwd)
        if (check != None) :
            return HttpResponse(check)
        user = Account.objects.filter(aid=aid)
        if len(user):
            return HttpResponse("卡号已经被注册")
        user = Account.objects.filter(tel=tel)
        if len(user):
            return HttpResponse("手机号已经被注册")
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        newacc = Account(aid=aid, pname=pname, pid=pid, pbirth=pbirth, psex=psex, tel=tel, logpwdhash=sha256(pwd.encode()).hexdigest(), regtime = formatted_time, balance = 0)
        newacc.save()
        return HttpResponse("success")
    return render(requests, 'reg.html',{'message':'test'})

def getinfo(token):
    coo = Cookie.objects.filter(cookie=token)
    aid = coo.values()[0]['uid']
    user = Account.objects.filter(aid=aid)
    info = user.values()[0]
    del info['logpwdhash']
    if info['psex']=='m':
        info['psex']='男'
    else:
        info['psex']='女'
    info['balance']=f"{info['balance']:.2f}"
    return info

def getname(aid):
    user = Account.objects.filter(aid=aid)
    if not len(user):
        return None
    return user.values()[0]['pname']

def record(requests):
    token = requests.COOKIES['token']
    aid = getinfo(token)['aid']
    rec0 = Record.objects.filter(orig_id=aid).values()
    rec1 = Record.objects.filter(recv_id=aid).values()
    orig_li = []
    for item in rec0:
        rec = {
            'orig':getname(item['orig_id']),
            'recv':getname(item['recv_id']),
            'money':f"{item['money']:.2f}",
            'time':item['time']
        }
        orig_li.append(rec)
    recv_li = []
    for item in rec1:
        rec = {
            'orig':getname(item['orig_id']),
            'recv':getname(item['recv_id']),
            'money':f"{item['money']:.2f}",
            'time':item['time']
        }
        recv_li.append(rec)
    context = {
        'orig':orig_li,
        'recv':recv_li
    }
    return render(requests,"record.html",context)

def trans(requests):
    return render(requests, "trans.html")