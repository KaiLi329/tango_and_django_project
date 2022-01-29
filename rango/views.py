from rango.models import Category, Page
from django.shortcuts import render
from django.http import HttpResponse


# import the Response from the django.http module

# index
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


# about
def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Kai Li'}

    return render(request, 'rango/about.html', context=context_dict)


# show_category
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)
