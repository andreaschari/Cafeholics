import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cafeholics.settings')
import django
django.setup()
from cafe.models import UserProfile, Cafe, Review
from django.contrib.auth.models import User
from cafeholics.settings import BASE_DIR, MEDIA_DIR
from django.core.files.images import ImageFile


def populate():
    # Firstly we create the lists of dictionaries containing
    # the coffee shop owners and the users who rate cafes.
    # Then we will create a dictionary of dictionaries for
    # the coffee shops and their reviews.
    cafe_owners = [{'username': 'xeniaskotti' ,'first_name': 'Xenia' , 'last_name':'Skotti', 'email': 'xeniaskotti@gmail.com', 'password': '1p2Qw#rT', 'owner': True},
                    {'username': 'alisonscott' ,'first_name': 'Alison' , 'last_name':'Scott', 'email': 'alisonscott@outlook.com', 'password': '5tB@e7Pl', 'owner':True},
                    {'username': 'jonathan23' ,'first_name': 'Jonathan' , 'last_name':'Holland', 'email': 'jonathan23@outlook.com', 'password': '!2FgA@pm', 'owner':True}]

    customers = [ {'username': 'jakehill' ,'first_name': 'Jake' , 'last_name':'Hill', 'email': 'jakehill@gmail.com', 'password': 'Sm&4R8pA', 'owner':False},
                    {'username': 'tomwalker' ,'first_name': 'Tom' , 'last_name':'Walker', 'email': 'tomwalker@gmail.com', 'password': '$pm%5td3', 'owner':False},
                    {'username': 'caroline99' ,'first_name': 'Caroline' , 'last_name':'Mcdonald', 'email': 'carolinemacdonald99@outlook.com', 'password': '2p#mT@!d', 'owner':False},
                    {'username': 'johnson34' ,'first_name': 'Johnson' , 'last_name':'Hill', 'email': 'johnsonhill@outlook.com', 'password': '!2FgA@pm', 'owner':False}]

    cafes = {'xeniaskotti': [{'cafe_name' : 'Free Spirit','pricepoint': 1, 'picture':ImageFile(open(MEDIA_DIR + r'/FreeSpirit.jpg','rb')), 'address': '66 Hyndland St, Glasgow G11 5PT', 'opening_hours': '9am to 5pm'},
                            {'cafe_name': 'CoffeeRiver', 'pricepoint': 2, 'picture':ImageFile(open(MEDIA_DIR +r'/CoffeeRiver.jpg','rb')), 'address': '7 Keith St, Glasgow G11 6QQ', 'opening_hours': '9am to 5pm'}],
            'alisonscott': [{'cafe_name' : 'Starbucks','pricepoint': 3,'picture': ImageFile(open(MEDIA_DIR +r'/Starbucks.jpg','rb')), 'address': '254 Byres Rd, Glasgow G12 8SH', 'opening_hours': '9am to 5pm'},
                            {'cafe_name': 'Monza', 'pricepoint': 1, 'picture': ImageFile(open(MEDIA_DIR +r'/Monza.jpg','rb')), 'address': '13 Vine St, Glasgow G11 6BA', 'opening_hours': '9am to 5pm'}],
            'jonathan23':[{'cafe_name' : 'Fika','pricepoint': 2, 'picture': ImageFile(open(MEDIA_DIR + r'/Fika.jpg','rb')), 'address': '579 Dumbarton Rd, Glasgow G11 6HY', 'opening_hours': '9am to 5pm'}]}

    reviews = {'Free Spirit': [{'customer_username':'jakehill', 'price': 1, 'service' : 2, 'atmosphere' : 3, 'quality': 3, 'waiting_time': 5},
                                {'customer_username':'tomwalker', 'price': 3, 'service' : 3, 'atmosphere' : 3, 'quality': 5, 'waiting_time': 5},
                                {'customer_username':'caroline99', 'price': 4, 'service' : 4, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 5},
                                {'customer_username':'johnson34', 'price': 3, 'service' : 4, 'atmosphere' : 4, 'quality': 2, 'waiting_time': 5}],
                'CoffeeRiver':[{'customer_username':'jakehill', 'price': 2, 'service' : 3, 'atmosphere' : 3, 'quality': 2, 'waiting_time': 3},
                            {'customer_username':'caroline99', 'price': 2, 'service' : 4, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 3},
                            {'customer_username':'tomwalker', 'price': 2, 'service' : 3, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 3},
                            {'customer_username':'johnson34', 'price': 2, 'service' : 2, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 3}],
                'Monza': [{'customer_username':'tomwalker', 'price': 2, 'service' : 2, 'atmosphere' : 4, 'quality': 2, 'waiting_time': 3},
                            {'customer_username':'caroline99', 'price': 4, 'service' : 4, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 5},
                            {'customer_username':'johnson34', 'price': 3, 'service' : 4, 'atmosphere' : 4, 'quality': 2, 'waiting_time': 5}],
                'Starbucks': [{'customer_username':'jakehill', 'price': 2, 'service' : 3, 'atmosphere' : 3, 'quality': 3, 'waiting_time': 5},
                            {'customer_username':'tomwalker', 'price': 3, 'service' : 3, 'atmosphere' : 3, 'quality': 4, 'waiting_time': 5},
                            {'customer_username':'caroline99', 'price': 4, 'service' : 4, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 5},
                            {'customer_username':'johnson34', 'price': 3, 'service' : 4, 'atmosphere' : 4, 'quality': 2, 'waiting_time': 5}],
                'Fika': [{'customer_username':'jakehill', 'price': 5, 'service' : 5, 'atmosphere' : 5, 'quality': 5, 'waiting_time': 5},
                            {'customer_username':'caroline99', 'price': 5, 'service' : 4, 'atmosphere' : 3, 'quality': 4, 'waiting_time': 5},
                            {'customer_username':'tomwalker', 'price': 5, 'service' : 5, 'atmosphere' : 5, 'quality': 4, 'waiting_time': 5},
                            {'customer_username':'johnson34', 'price': 5, 'service' : 4, 'atmosphere' : 4, 'quality': 5, 'waiting_time': 5}]
                            }

    users =  {}
    for customer_data in customers:
        c = add_user(customer_data["username"], customer_data["first_name"], customer_data["last_name"], customer_data["email"], customer_data["password"], customer_data["owner"])
        users[customer_data["username"]] = c

    for owner_data in cafe_owners:
        o = add_user(owner_data["username"], owner_data["first_name"], owner_data["last_name"], owner_data["email"], owner_data["password"], owner_data["owner"])
        for cafe in cafes[owner_data["username"]]:
            c = add_cafe(o, cafe["cafe_name"], cafe["pricepoint"], cafe['address'], cafe['opening_hours'], cafe['picture'])
            for review in reviews[cafe["cafe_name"]]:
                r = add_review(c, users[review["customer_username"]],review["price"],review["service"],review["atmosphere"],review["quality"], review["waiting_time"])

    for c in Cafe.objects.all():
        c.avg_rating = avg_rating_cafe(c)
        c.save()

def add_user(username, first_name, last_name, email, password, owner):
    u = User.objects.get_or_create(username = username, first_name = first_name, last_name = last_name, email = email, password = password )[0]
    up = UserProfile.objects.get_or_create(user = u, is_owner = owner)[0]
    up.save()
    return up


def add_cafe(owner,cafe_name,pricepoint,address, opening_hours,picture):
    c = Cafe.objects.get_or_create(owner = owner, name = cafe_name, pricepoint = pricepoint)[0]
    print(picture)
    c.picture = picture
    c.opening_hours = opening_hours
    c.address = address
    c.save()
    return c


def add_review(cafe,user,price,service,atmosphere,quality,waiting_time):
    r = Review.objects.get_or_create(cafe=cafe,user=user, price=price, service=service, atmosphere=atmosphere, quality=quality, waiting_time=waiting_time)[0]
    r.avg_rating = int((r.price + r.service + r.atmosphere + r.waiting_time + r.quality)/5)
    r.save()
    return r

def avg_rating_cafe(cafe):
    review = Review.objects.filter(cafe=cafe)
    review_sum, count = 0, 0
    avg = 0
    for r in review:
        review_sum += r.avg_rating
        count = count+1
    if (count>0):
        avg = review_sum / count
    return avg

if __name__ == '__main__':
    # print("Starting Cafe population script...")
    # print("Users created:")
    # for u in UserProfile.objects.all():
    #     print(str(u))
    #
    # print()
    # print("Cafes created:")
    # for c in Cafe.objects.all():
    #     print(str(c))
    #     print("Customers who left a review:")
    #     for r in Review.objects.filter(cafe=c):
    #         print(str(r))
    #     print()
    print(MEDIA_DIR + r'\FreeSpirit.jpg')
    populate()
