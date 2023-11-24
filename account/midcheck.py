from django.shortcuts import render
from account.models import Account,Cookie
from django.http import *
from hashlib import sha256
import secrets
import time

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, requests):
        if requests.path == "/login/":
            return self.get_response(requests)
        try:
            token = requests.COOKIES['token']
        except:
            return HttpResponseRedirect("/login/")
        
        if not self.check_token(token):
            return HttpResponseRedirect("/login/")

        response = self.get_response(requests)
        return response

    def check_token(self, token):
        coo = Cookie.objects.filter(cookie=token)
        if not len(coo):
            return False
        aid = coo.values()[0]['uid']
        live = float(coo.values()[0]['live'])
        if time.time() > live:
            return False
        return True