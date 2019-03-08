from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from cafe.models import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os, socket
import populate_cafe


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


class AdminPageTest(StaticLiveServerTestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(3)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(AdminPageTest, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def test_population_script(self):
        # Populate database
        populate_cafe.populate()
        url = self.live_server_url
        self.browser.get(url + reverse('admin:index'))

        # Log in the admin page
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # check that the cafes were saved by the population script
        self.browser.get(self.live_server_url + '/admin/cafe/cafe')
        self.browser.find_elements_by_partial_link_text('Free Spirit')
        self.browser.find_elements_by_partial_link_text('Starbucks')
        self.browser.find_elements_by_partial_link_text('Fika')
        self.browser.find_elements_by_partial_link_text('CoffeeRiver')
        self.browser.find_elements_by_partial_link_text('Monza')

        # check that the users were saved by the population script
        self.browser.get(self.live_server_url + '/admin//auth/user/')
        self.browser.find_elements_by_partial_link_text('jakehill')
        self.browser.find_elements_by_partial_link_text('tomwalker')
        self.browser.find_elements_by_partial_link_text('caroline99')

        # check that the owners were saved by the population script
        self.browser.find_elements_by_partial_link_text('xeniaskotti')
        self.browser.find_elements_by_partial_link_text('alisonscott')
        self.browser.find_elements_by_partial_link_text('jonathan23')

    def test_admin_page_contains_cafes(self):
        populate_cafe.populate()
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('admin:index'))

        # login to admin page
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Click in Cafes
        pages_link = self.browser.find_element_by_link_text('Cafes')
        pages_link.click()

        body = self.browser.find_element_by_tag_name('body')

        # Get all cafes
        cafes = Cafe.objects.all()

        # Check that all cafes owner, name and pricepoint are displayed
        for cafe in cafes:
            self.assertIn(str(cafe.owner), body.text)
            self.assertIn(str(cafe.name), body.text)
            self.assertIn(str(cafe.pricepoint), body.text)

    def test_admin_page_contains_reviews(self):
        populate_cafe.populate()
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('admin:index'))

        # login to admin page
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Click in Cafes
        pages_link = self.browser.find_element_by_link_text('Reviews')
        pages_link.click()

        body = self.browser.find_element_by_tag_name('body')

        reviews = Review.objects.all()
        # check that all review cafe, user and comments are displayed
        for review in reviews:
            self.assertIn(str(review.cafe), body.text)
            self.assertIn(str(review.user), body.text)
            self.assertIn(str(review.comments), body.text)

    # TODO: add test for new cafe, new review,
    #  check that population script changes the database

    def test_can_create_new_cafe_via_admin_page(self):
        pass

    def test_can_create_new_review_via_admin_page(self):
        pass

    def test_population_script_changes_database(self):
        pass
