from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from cafe.forms import CafeForm, ReviewForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cafe.models import *
import django.core.exceptions


def home(request):
    cafe_list = Cafe.objects.all()
    Cafe.objects.order_by('-avg_rating')[:10]
    context_dict = {'cafes': cafe_list}

    return render(request, 'cafe/home.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': "This is the about page "}

    return render(request, 'cafe/about.html', context=context_dict)


def cafes(request):
    cafe_list = Cafe.objects.all()
    price_list = Cafe.objects.order_by('review__price')
    service_list = Cafe.objects.order_by('review__service')
    atmosphere_list = Cafe.objects.order_by('review__atmosphere')
    quality_list = Cafe.objects.order_by('review__quality')
    waiting_times_list = Cafe.objects.order_by('review__waiting_time')
    context_dict = {'cafes': cafe_list, 'byPrice': price_list, 'byService': service_list,
                    'byAtmosphere': atmosphere_list, 'byQuality': quality_list,
                    'byWaitingTimes': waiting_times_list}

    return render(request, 'cafe/cafes.html', context=context_dict)


def chosen_cafe(request, cafe_name_slug):
    context_dict = {}
    try:
        cafe = Cafe.objects.get(slug=cafe_name_slug)
        reviews = Review.objects.order_by('-pub_date').filter(cafe=cafe)
        name = cafe.name
        pricepoint = cafe.pricepoint
        owner = cafe.owner
        picture = cafe.picture
        context_dict['name'] = name
        context_dict['reviews'] = reviews
        context_dict['cafe'] = cafe
        context_dict['pricepoint'] = pricepoint
        context_dict['owner'] = owner
        context_dict['picture'] = picture
        return render(request, 'cafe/chosen_cafe.html', context=context_dict)
    except Cafe.DoesNotExist:
        context_dict['errors'] = 'This Cafe Does Not Exist'
        return render(request, 'cafe/cafes.html', context=context_dict)


def add_cafe(request):
    form = CafeForm()
    if request.method == 'POST':
        form = CafeForm(data=request.POST)

        if form.is_valid():
            cafe = form.save(commit=False)
            cafe.owner = request.user
            if 'picture' in request.FILES:
                cafe.picture = request.FILES['picture']
            cafe.save()
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
            return HttpResponse("Invalid login details supplied."), HttpResponseRedirect(reverse('login'))

    else:
        return render(request, 'cafe/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def my_account(request):
    context_dict = {}
    try:
        user = User.objects.get(username=request.user)
        context_dict["username"] = user.username
        context_dict["first_name"] = user.first_name
        context_dict["last_name"] = user.last_name
        context_dict["email"] = user.email
        context_dict["is_owner"] = user.userprofile.is_owner
        return render(request, 'cafe/my_account.html', context=context_dict)
    except User.DoesNotExist:
        return redirect('/')


@login_required
def delete_account(request):
    UserProfile.objects.filter.get(request.user.get_username()).delete()
    return redirect('/')


@login_required
def my_reviews(request):
    user = UserProfile.objects.get(user=request.user)
    reviews_list = Review.objects.filter(user=user)
    return render(request, 'cafe/my_review.html', {'reviews_list': reviews_list})

@login_required
def my_cafes(request):
    if request.user.is_owner:
        cafe_list = Cafe.objects.filter(user=request.user)

    return render(request, 'cafe/my_cafes.html', {'cafe_list':cafe_list})
@login_required
def edit_cafe(request, cafe_name_slug):
    context_dict ={}
    try:
        cafe = Cafe.objects.get(slug=cafe_name_slug)
    except Cafe.DoesNotExist:
        cafe = None

    if cafe:
        context_dict={'cafe.owner':cafe.owner,'cafe.name':cafe.name,'cafe.picture':cafe.picture,
                      'cafe.pricepoint.':cafe.pricepoint, 'cafe.description':cafe.description}

    return render(request, 'cafe/edit_cafe.html', context=context_dict)


def delete_cafe(request, cafe_name_slug):
    try:
        cafe =Cafe.objects.get(slug=cafe_name_slug)
    except Cafe.DoesNotExist:
        cafe = None
    if cafe:
        cafe.delete()
    return redirect('/')

@login_required
def write_review(request, cafe_name_slug):
    try:
        cafe = Cafe.objects.get(slug=cafe_name_slug)
    except Cafe.DoesNotExist:
        return render(request, 'cafe/cafes.html', {'errors': 'One Does not simply review a non-existing page'})
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            if cafe:
                review = form.save(commit=False)
                review.cafe = cafe
                review.avg_rating = int((review.price+review.quality+review.waiting_time+review.service+review.atmosphere )/5)
                review.user = request.user
                review.save()
        else:
            print(form.errors)

    return render(request, 'cafe/write_review.html', {'form': form})

@login_required
def edit_review(request, cafe_name_slug):
    try:
        cafe =Cafe.objects.get(slug=cafe_name_slug)
    except Cafe.DoesNotExist:
        cafe = None
    if cafe:
        toedit = Review.objects.get(cafe=cafe_name_slug,user=request.user)
        context_dict={'toedit.atmosphere':toedit.atmosphere, 'toedit.service':toedit.service,
                      'toedit.quality':toedit.quality, 'toedit.price':toedit.price,
                      'toedit.waiting_time':toedit.waiting_time}
    return render(request, 'cafe/edit_review.html', context=context_dict)


@login_required
def delete_review(request, cafe_name_slug):
    try:
        cafe =Cafe.objects.get(slug=cafe_name_slug)
    except Cafe.DoesNotExist:
        cafe = None
    if cafe:
        Review.objects.get(cafe=cafe,user=request.user).delete()
    return redirect('/')


def search(request):
    if request.method == 'GET':
        cafe_name = request.GET.get('search')

        try:
            #name = Cafe.name
            status = Cafe.objects.get(name__icontains=cafe_name)
            return render(request, 'cafe/search.html', {'cafes': status})
        except Exception:
            print("Can't get cafe names")
    else:
        return render(request, 'cafe/search.html', {})
