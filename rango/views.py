from rango.models import Category
from django.shortcuts import render
from django.http import HttpResponse


# import the Response from the django.http module

def index(request):
    # Query the database for a list of ALL categories currently stored
    # Order the categories by the number of likes (descending order)
    # Retrieve top 5 only
    # Place the list in context_dict
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    #             request    template file name   context dictionary
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Kai Li'}

    return render(request, 'rango/about.html', context=context_dict)
