from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import UpdateView
from django.urls import reverse
from cafe.forms import *
from cafe.models import *
from django.shortcuts import get_object_or_404


class EditCafeView(UpdateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'cafe/edit_cafe.html'

    def get_object(self, *args, **kwargs):
        return Cafe.objects.get(slug=self.kwargs['cafe_name_slug'])

    def get_success_url(self, *args, **kwargs):
        return reverse('my_cafes')


class EditReviewView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'cafe/edit_review.html'

    def get_object(self, *args, **kwargs):
        cafe = Cafe.objects.get(slug=self.kwargs['cafe_name_slug'])
        current_user = UserProfile.objects.all().get(user=self.request.user)
        return Review.objects.get(cafe=cafe, user=current_user)

    def get_success_url(self, *args, **kwargs):
        return reverse('my_reviews')


def home(request):
    context_dict = {}
    if 'search' in request.GET:
        search_term = request.GET['search']
        cafes_found = Cafe.objects.all().filter(name__icontains=search_term)
        context_dict['cafes'] = cafes_found
        return render(request, 'cafe/search_results.html', context=context_dict)
    cafe_list = Cafe.objects.order_by('-avg_rating')[:10]
    context_dict['cafes'] = cafe_list

    return render(request, 'cafe/home.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': "This is the about page "}

    return render(request, 'cafe/about.html', context=context_dict)


def sort_by_category_lists(cafe_list):
    price_list, service_list, atmosphere_list, quality_list, waiting_times_list = [], [], [], [], []
    by_price, by_service, by_atmosphere, by_waiting_times, by_quality = [], [], [], [], []
    for cafe in cafe_list:
        reviews = Review.objects.filter(cafe=cafe)
        sum_price, sum_quality, sum_waiting_time, sum_service, sum_atmosphere, count = 0, 0, 0, 0, 0, 0
        for review in reviews:
            sum_price += review.price
            sum_quality += review.quality
            sum_waiting_time += review.waiting_time
            sum_service += review.service
            sum_atmosphere += review.atmosphere
            count += 1
        if count > 0:
            price_list.append([sum_price/count, cafe.name])
            quality_list.append([sum_quality/count, cafe.name])
            waiting_times_list.append([sum_waiting_time/count, cafe.name])
            service_list.append([sum_service/count, cafe.name])
            atmosphere_list.append([sum_atmosphere/count, cafe.name])
    price_list.sort()
    quality_list.sort()
    waiting_times_list.sort()
    service_list.sort()
    atmosphere_list.sort()

    for i in range(len(price_list)):
        by_price.append(price_list[i][1])
        by_service.append(service_list[i][1])
        by_atmosphere.append(atmosphere_list[i][1])
        by_quality.append(quality_list[i][1])
        by_waiting_times.append(waiting_times_list[i][1])

    for cafe in cafe_list:
        for i in range(len(by_price)):
            if by_price[i] == cafe.name:
                by_price[i] = cafe
            if by_quality[i] == cafe.name:
                by_quality[i] = cafe
            if by_service[i] == cafe.name:
                by_service[i] = cafe
            if by_atmosphere[i] == cafe.name:
                by_atmosphere[i] = cafe
            if by_waiting_times[i] == cafe.name:
                by_waiting_times[i] = cafe

    return by_quality, by_service, by_atmosphere, by_waiting_times, by_price


def cafes(request):
    context_dict = {}
    if 'search' in request.GET:
        search_term = request.GET['search']
        cafes_found = Cafe.objects.all().filter(name__icontains=search_term)
        context_dict['cafes'] = cafes_found
        return render(request, 'cafe/search_results.html', context=context_dict)
    cafe_list = Cafe.objects.all()
    by_quality, by_service, by_atmosphere, by_waiting_times, by_price = sort_by_category_lists(cafe_list)
    avg_rating_list = Cafe.objects.order_by('-avg_rating')
    context_dict = {'cafes': cafe_list, 'by_price': by_price, 'by_service': by_service,
                    'by_atmosphere': by_atmosphere, 'by_quality': by_quality,
                    'by_waiting_times': by_waiting_times, 'by_average': avg_rating_list}

    return render(request, 'cafe/cafes.html', context=context_dict)


def chosen_cafe(request, cafe_name_slug):
    context_dict = {}
    try:
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            context_dict['user'] = user
        cafe = Cafe.objects.get(slug=cafe_name_slug)
        reviews = Review.objects.order_by('-pub_date').filter(cafe=cafe)
        if len(reviews) > 0:
            context_dict['reviews'] = reviews
            context_dict['avg rating'] = avg_rating_cafe(cafe_name_slug)
        else:
            context_dict['avg rating'] = 0
        context_dict['opening_hours'] = cafe.opening_hours
        context_dict['name'] = cafe.name
        context_dict['pricepoint'] = cafe.pricepoint
        context_dict['owner'] = cafe.owner
        context_dict['picture'] = cafe.picture
        context_dict['cafe'] = cafe
        return render(request, 'cafe/chosen_cafe.html', context=context_dict)
    except Cafe.DoesNotExist:
        context_dict['errors'] = 'This Cafe Does Not Exist'
        return render(request, 'cafe/cafes.html', context=context_dict)


def avg_rating_cafe(cafe_name_slug):
    cafe = Cafe.objects.get(slug=cafe_name_slug)
    review = Review.objects.filter(cafe=cafe)
    review_sum, count = 0, 0
    for r in review:
        review_sum += r.avg_rating
        count = count+1
    avg = review_sum / count
    return avg


@login_required
def add_cafe(request):
    form = CafeForm()
    if request.method == 'POST':
        form = CafeForm(request.POST, request.FILES)

        if form.is_valid():
            cafe = form.save(commit=False)
            cafe.owner = UserProfile.objects.get(user=request.user)
            cafe.picture = form.cleaned_data['picture']
            cafe.save()
            return redirect('/cafe/my_account/my_cafes')
        else:
            print(form.errors)
    return render(request, 'cafe/add_cafe.html', {'form': form})


def sign_up(request):
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
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/cafe')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/sign_up.html', {'user_form': user_form, 'profile_form': profile_form})


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
def delete_account(request, username):
    User.objects.all().filter(username=username).delete()
    return redirect('/')


@login_required
def my_reviews(request):
    user = UserProfile.objects.get(user=request.user)
    reviews_list = Review.objects.filter(user=user)

    return render(request, 'cafe/my_reviews.html', {'reviews_list': reviews_list})


@login_required
def my_cafes(request):
    user = UserProfile.objects.get(user=request.user)
    cafe_list = Cafe.objects.filter(owner=user)
    return render(request, 'cafe/my_cafes.html', {'cafe_list': cafe_list})


@login_required
def delete_cafe(request, cafe_name_slug):
    # if request.method == 'POST':
        cafe = Cafe.objects.all().filter(slug=cafe_name_slug)
        # print(cafe.name)
        get_object_or_404(cafe, slug=cafe_name_slug).delete()
        return redirect('/cafe/my_account/my_cafes/')


@login_required
def write_review(request, cafe_name_slug):
    context_dict = {}
    try:
        cafe = Cafe.objects.get(slug=cafe_name_slug)
    except Cafe.DoesNotExist:
        return render(request, 'cafe/cafes.html', {'errors': 'One Does not simply review a non-existing page'})
    context_dict['cafe'] = cafe
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cafe = cafe
            review.avg_rating = int((review.price+review.quality+review.waiting_time+review.service+review.atmosphere)/5)
            review.user = UserProfile.objects.get(user=request.user)
            review.save()
            return redirect('/cafe/my_account/my_reviews')
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'cafe/write_review.html', context_dict)


@login_required
def delete_review(request, cafe_name_slug):
    try:
        cafe = Cafe.objects.all().get(slug=cafe_name_slug)
        current_user = UserProfile.objects.all().get(user=request.user)
        cafe_reviews = Review.objects.all().filter(user=current_user)
        cafe_reviews.get(cafe=cafe).delete()
    except Cafe.DoesNotExist:
        cafe = None
    except Review.DoesNotExist:
        cafe_reviews = None
    finally:
        return redirect('/cafe/my_account/my_reviews/')


def search(request):
    context_dict = {}
    if 'search' in request.GET:
        search_term = request.GET['search']
        cafes_found = Cafe.objects.all().filter(name__icontains=search_term)
        context_dict['cafes'] = cafes_found
        return render(request, 'cafe/search_results.html', context=context_dict)
    if request.method == 'GET':
        cafe_name = request.GET.get('search')

        try:
            status = Cafe.objects.filter(name__icontains=cafe_name)
            return render(request, 'cafe/search_results.html', {'cafes': status})
        except Cafe.DoesNotExist:
            print("Can't get cafe names")
    else:
        return render(request, 'cafe/search_results.html', {})
