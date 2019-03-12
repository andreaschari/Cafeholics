from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cafe.forms import Cafe, CafeForm, ReviewForm, UserForm, UserProfileForm, Review
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def home(request):
    cafe_list = Cafe.objects.all()
    #Cafe.objects.order_by('-average_rating')[:10]
    context_dict = {'cafes': cafe_list}
    # for cafe in cafe_list:
    #    Review.atmosphere + Review.service +

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
        reviews = Review.objects.order_by().filter(cafe=cafe) #order by time but no time parameter?
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
    except cafe.DoesNotExist:
        context_dict['name'] = None
        context_dict['cafe'] = None
        context_dict['review'] = None
        context_dict['pricepoint'] = None
        context_dict['owner'] = None
        context_dict['picture'] = None
    return render(request, 'cafe/chosen_cafe.html', context=context_dict)


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
        user = UserForm.objects.get(user=request.user)
        context_dict["username"] = user.username
        context_dict["first_name"] = user.first_name
        context_dict["last_name"] = user.last_name
        context_dict["email"] = user.email

    except user.DoesNotExist:
        context_dict["username"] = None
        context_dict["first_name"] = None
        context_dict["last_name"] = None
        context_dict["email"] = None

    return render(request, 'cafe/my_account.html', context=context_dict)

@login_required
def my_reviews(request):
    reviews_list = Review.objects.filter(user=request.user)
    return render(request, 'cafe/my_review.html', {'reviews_list':reviews_list})

@login_required
def my_cafes(request):
    if request.user.is_owner:
        cafe_list = Cafe.objects.filter(user=request.user)

    return render(request, 'cafe/my_cafes.html', {'cafe_list':cafe_list})

@login_required
def write_review(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return render(request, 'cafe/write_review.html', {'form':form})

def search(request):
    if request.method == 'GET':
        cafe_name = request.GET.get('search')

        try:
            status = Cafe.objects.get((Cafe.name)__icontains)

        except:




