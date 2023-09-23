from django.shortcuts import render

# Create your views here.
def home(requests):
    context = {
        'username' : 'test',
    }

    return render(requests,'home.html',context)

def login(requests):
    context = {}

    return render(requests, 'login.html', context)