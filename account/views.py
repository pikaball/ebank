from django.shortcuts import render
from account.models import Account
from django.http import HttpRequest,HttpResponse

# Create your views here.
def home(requests):
    context = {
        'username' : 'test',
    }
    return render(requests,'home.html',context)

def login(requests):
    context = {}

    return render(requests, 'login.html', context)