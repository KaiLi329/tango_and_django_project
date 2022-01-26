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
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
