from datetime import datetime
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse


# import the Response from the django.http module

# index
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


# about
def about(request):
    visitor_cookie_handler(request)
    context_dict = {
        'visits': request.session['visits'],
    }
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


# add category
@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category
            form.save(commit=True)
            # redirect the user back to index view
            return redirect(reverse('rango:index'))
        else:
            # The supplied form contained errors
            print(form.errors)

    # Render the form with error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})


# add page
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # you cannot add a page to a category that does not exist
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


# cookie helper func
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.COOKIES.get(cookie)
    if not val:
        val = default_val
    return val


# cookie setting
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', 1))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than one day since the last visit
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # update/set the visits cookie
    request.session['visits'] = visits


# register
def register(request):
    # A boolean value for telling the template whether the registration was successful
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the row form information
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save
            user = user_form.save()

            # Hash the password with set_password method
            user.set_password(user.password)
            user.save()

            # Sort out the UserProfile instance
            # Since we need to set the user attribute ourselves
            # we set commit=False, This delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile pic?
            # If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update the boolean variable
            registered = True
        else:
            # Invalid form or forms - mistake or sth else
            # Print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, render our form using two ModelForm instance
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


# Login
def user_login(request):
    # HTTP POST?
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # information obtained from the login form
        # user request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None if the value does not exist,
        # while request.POST.get['<variable>'] will raise a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - A User object is returned if it is
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct
        # If None, no user with matching credentials was found
        if user:
            # Is the account active?
            if user.is_active:
                # If the account is valid and active, then we can log the user in
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # An inactive account was used - denied
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details are provided
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # No context variables to pass to the template system, hence the blank dictionary object
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
    # return HttpResponse("Since you're logged in, you can see this text")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
