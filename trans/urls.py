from django.urls import path
from . import views

urlpatterns = [
    path("trans/",views.deal,name="trans"),
]