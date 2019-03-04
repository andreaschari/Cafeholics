from django.test import TestCase
from cafe.models import *


class CafeModelTest(TestCase):

    def setUp(self):
        # create test owner
        self.user = User.objects.create_user(username='test_owner', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=True)
        # login as test owner
        login = self.client.login(username='test_owner', password='12345')

    def test_can_create_cafe(self):
        # create test cafe
        cafe = Cafe(owner=self.user_profile, name='Cafe One', pricepoint=2)
        cafe.save()
        # check if cafe exists in database
        cafes_in_database = Cafe.objects.all()
        self.assertEquals(len(cafes_in_database), 1)
        cafe_in_database = cafes_in_database[0]
        self.assertEquals(cafe_in_database, cafe)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Cafe._meta.verbose_name_plural), "Cafes")

    def test_str_representation(self):
        # create test cafe
        cafe = Cafe(owner=self.user_profile, name='Cafe One', pricepoint=2)
        cafe.save()
        # check if the __str__ method return the cafe's name
        self.assertEqual(str(cafe), cafe.name)

    def tearDown(self):
        self.user.delete()


class ReviewModelTest(TestCase):
    def setUp(self):
        # create test owner
        self.owner = User.objects.create_user(username='test_owner', password='12345')
        self.owner_profile = UserProfile.objects.create(user=self.owner, is_owner=True)
        # create and login with test user
        self.user = User.objects.create_user('foo', 'bar')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=False)
        self.client.login(username='foo', password='bar')
        # create and save test cafe
        self.cafe = Cafe(owner=self.owner_profile, name='Cafe One', pricepoint=2)
        self.cafe.save()

    def test_can_create_review(self):
        # create test review
        review = Review(cafe=self.cafe, user=self.user_profile,
                        price=2, service=3, atmosphere=4, quality=2, waiting_time=1)
        review.save()
        # check if review exists in database
        reviews_in_database = Review.objects.all()
        self.assertEquals(len(reviews_in_database), 1)
        review_in_database = reviews_in_database[0]
        self.assertEquals(review_in_database, review)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Review._meta.verbose_name_plural), "Reviews")

    def test_user_cannot_review_same_cafe_twice(self):
        from django.db import IntegrityError
        # create test reviews check if an error is raised
        with self.assertRaises(IntegrityError):
            review_one = Review(cafe=self.cafe, user=self.user_profile,
                            price=2, service=3, atmosphere=4, quality=2, waiting_time=1)
            review_one.save()
            review_two = Review(cafe=self.cafe, user=self.user_profile,
                            price=5, service=1, atmosphere=4, quality=3, waiting_time=1)
            review_two.save()
