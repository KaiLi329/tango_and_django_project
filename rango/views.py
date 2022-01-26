from django.shortcuts import render
from django.http import HttpResponse


# import the Response from the django.http module

def index(request):
    return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")


def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
