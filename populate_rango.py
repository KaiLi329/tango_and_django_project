import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
    # Create lists of dictionaries containing the pages
    # add into each category
    # create a dictionary of dictionaries for our categories
    # through each data structure, and add the data to our models

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/'},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorial/python/'},

    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/'},
    ]

    other_page = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org'},
    ]

    cats = {'Python': {'pages': python_pages},
            'Django': {'pages': django_pages},
            'Other Frameworks': {'pages': other_page},
            }

    # The code below goes through the cat dictionaries, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, views=888)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name):
    if name == 'Python':
        c = Category.objects.get_or_create(name=name, views=128, likes=64)[0]
    elif name == 'Django':
        c = Category.objects.get_or_create(name=name, views=64, likes=32)[0]
    else:
        c = Category.objects.get_or_create(name=name, views=32, likes=16)[0]

    c.save()
    return c


# Start execution
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
