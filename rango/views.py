from django.shortcuts import render
from django.http import HttpResponse


# import the Response from the django.http module

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    #             request    template file name   context dictionary
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Kai Li'}

    return render(request, 'rango/about.html', context=context_dict)
