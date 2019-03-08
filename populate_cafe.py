import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cafeholics.settings')

import django
django.setup()
from cafe.models import UserProfile, Cafe, Review
from django.contrib.auth.models import User


def populate():
    # Firstly we create the lists of dictionaries containing
    # the coffe shop owners and the users who rate cafes.
    # Then we will create a dictionary of dictionaries for
    # the coffee shops and their reviews.

    cafe_owners = [{'username': 'xeniaskotti' ,'first_name': 'Xenia' , 'last_name':'Skotti', 'email': 'xeniaskotti@gmail.com', 'password': '1p2Qw#rT', 'owner': True},
                    {'username': 'alisonscott' ,'first_name': 'Alison' , 'last_name':'Scott', 'email': 'alisonscott@outlook.com', 'password': '5tB@e7Pl', 'owner':True},
                    {'username': 'jonathan23' ,'first_name': 'Jonathan' , 'last_name':'Holland', 'email': 'jonathan23@outlook.com', 'password': '!2FgA@pm', 'owner':True}]

    customers = [ {'username': 'jakehill' ,'first_name': 'Jake' , 'last_name':'Hill', 'email': 'jakehill@gmail.com', 'password': 'Sm&4R8pA', 'owner':False},
                    {'username': 'tomwalker' ,'first_name': 'Tom' , 'last_name':'Walker', 'email': 'tomwalker@gmail.com', 'password': '$pm%5td3', 'owner':False},
                    {'username': 'caroline99' ,'first_name': 'Caroline' , 'last_name':'Mcdonald', 'email': 'carolinemacdonald99@outlook.com', 'password': '2p#mT@!d', 'owner':False},]


    cafes = {'xeniaskotti': [{'cafe_name' : 'Free Spirit','pricepoint': 1}, {'cafe_name': 'CoffeeRiver', 'pricepoint': 2}],
                'alisonscott': [{'cafe_name' : 'Starbucks','pricepoint': 3}, {'cafe_name': 'Monza', 'pricepoint': 1}],
                'jonathan23':[{'cafe_name' : 'Fika','pricepoint': 2}]}

    reviews = {'Free Spirit': [{'customer_username':'jakehill', 'price': 1, 'service' : 2, 'atmosphere' : 3, 'quality': 3, 'waiting_time': 5},
                {'customer_username':'tomwalker', 'price': 3, 'service' : 3, 'atmosphere' : 3, 'quality': 5, 'waiting_time': 5}],
                'CoffeeRiver':[{'customer_username':'jakehill', 'price': 5, 'service' : 3, 'atmosphere' : 3, 'quality': 4, 'waiting_time': 5},
                            {'customer_username':'caroline99', 'price': 4, 'service' : 4, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 5}],
                'Monza': [{'customer_username':'tomwalker', 'price': 3, 'service' : 5, 'atmosphere' : 4, 'quality': 4, 'waiting_time': 5},
                            {'customer_username':'caroline99', 'price': 4, 'service' : 4, 'atmosphere' : 2, 'quality': 2, 'waiting_time': 5}],
                'Starbucks': [{'customer_username':'jakehill', 'price': 2, 'service' : 3, 'atmosphere' : 3, 'quality': 3, 'waiting_time': 5},
                            {'customer_username':'tomwalker', 'price': 3, 'service' : 3, 'atmosphere' : 3, 'quality': 4, 'waiting_time': 5}],
                'Fika': [{'customer_username':'jakehill', 'price': 5, 'service' : 5, 'atmosphere' : 5, 'quality': 5, 'waiting_time': 5},
                            {'customer_username':'caroline99', 'price': 5, 'service' : 4, 'atmosphere' : 3, 'quality': 4, 'waiting_time': 5}]
                            }
#what is the meaning of price relating to stars and the rest of the attributes

    #create the customers
    users =  {}
    for customer_data in customers:
        c = add_user(customer_data["username"], customer_data["first_name"], customer_data["last_name"], customer_data["email"], customer_data["password"], customer_data["owner"])
        users[customer_data["username"]] = c

    for owner_data in cafe_owners:
        o = add_user(owner_data["username"], owner_data["first_name"], owner_data["last_name"], owner_data["email"], owner_data["password"], owner_data["owner"])
        for cafe in cafes[owner_data["username"]]:
            c = add_cafe(o, cafe["cafe_name"], cafe["pricepoint"])
            for review in reviews[cafe["cafe_name"]]:
                r = add_review(c, users[review["customer_username"]],review["price"],review["service"],review["atmosphere"],review["quality"], review["waiting_time"])
    print("Users created:")
    for u in UserProfile.objects.all():
        print(str(u))

    print()
    print("Cafes created:")
    for c in Cafe.objects.all():
        print(str(c))
        print("Customers who left a review:")
        for r in Review.objects.filter(cafe = c):
            print(str(r))
        print()



def add_user(username, first_name, last_name, email, password, owner):
    u = User.objects.get_or_create(username = username)[0]
    u.first_name = first_name
    u.last_name = last_name
    u.email = email
    u.password = password
    up = UserProfile.objects.get_or_create(user = u, is_owner = owner)[0]
    up.save()
    return up

def add_cafe(owner,cafe_name,pricepoint):
    c = Cafe.objects.get_or_create(owner = owner, name = cafe_name, pricepoint = pricepoint)[0]
    c.save()
    return c

def add_review(cafe,user,price,service,atmosphere,quality,waiting_time):
    r = Review.objects.get_or_create(cafe=cafe,user=user, price=price, service=service, atmosphere=atmosphere, quality=quality, waiting_time=waiting_time)[0]
    r.save()
    return r

if __name__ == '__main__':
    print("Starting Cafe population scirpt...")
    populate()
