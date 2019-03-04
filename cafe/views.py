from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cafe.forms import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    cafe_list = Cafe.objects.order_by('-average rating') [:10]
    context_dict = {'cafes': cafe_list}

    return render(request, 'cafe/home.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': "This is the about page "}

    return render(request, 'cafe/about.html', context=context_dict)


def cafes(request):
    context_dict = {}

    return render(request, 'cafe/cafes.html', context=context_dict)


def chosen_cafe(request, cafe_name_slug):
    context_dict = {}
    try:
        cafe = Cafe.objects.get(slug=cafe_name_slug)
        reviews = Review.objects.filter(cafe=cafe)
        context_dict['reviews'] = reviews
        context_dict['cafe'] = cafe
    except Cafe.DoesNotExist:
        context_dict['cafe'] = None
        context_dict['review'] = None
    return render(request, 'cafe/chosen_cafe.html', context=context_dict)


def add_cafe(request):
    form = CafeForm()
    if request.method == 'POST':
        form = CafeForm(request.POST)

        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()

            form.save(commit=True)
            return home(request)

        else:
            print(form.errors)

    return render(request, 'cafe/upload_cafe.html', {'form': form})


def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'cafe/sign_up.html', {'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
            return HttpResponseRedirect(reverse('login'))

    else:
        return render(request, 'cafe/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def my_account(request):
    context_dict = {}

    return render(request, 'cafe/my_account.html', context=context_dict)
