from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login, name='login'),
    path("record/",views.record, name='record'),
    path("trans/",views.trans, name='trans'),
    path("register/", views.register, name="register")
]