import os
import socket
import populate_cafe
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from cafe.models import *
from django.conf import settings
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


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

    def test_cafe_contains_slug_field(self):
        # create test cafe
        cafe = Cafe(owner=self.user_profile, name='Cafe One', pricepoint=2)
        cafe.save()
        # check if slug was indeed saved
        self.assertEquals(cafe.slug, 'cafe-one')

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

    def test_admin_contains_user_profile(self):
        # Access admin page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('admin:index'))

        # Log in the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # Types username and password
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Check exists a link to user profiles
        self.browser.find_element_by_link_text('Users').click()

        # Create a user
        user = User.objects.get_or_create(username="johndoe", password="test1234",
                                          first_name="John", last_name="Doe")[0]
        user.set_password(user.password)
        user.save()
        # Create a user profile
        user_profile = UserProfile.objects.get_or_create(user=user, is_owner=False)[0]
        user_profile.save()
        self.browser.refresh()

        # Check there is one profile
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(user.username, body.text)

    def test_can_create_new_cafe_via_admin_page(self):
        # Access admin page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('admin:index'))

        # Check if it displays admin message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # login to admin page
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # check the Site Administration page exists
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # Check if is there link to Cafes and click it.
        cafe_link = self.browser.find_elements_by_partial_link_text('Caf')
        self.assertEquals(len(cafe_link), 1)
        cafe_link[0].click()

        # it's empty, so check for the empty message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 caf', body.text.lower())

        # Add a cafe by clicking on 'Add cafe'
        new_cafe_link = self.browser.find_element_by_class_name('addlink')
        new_cafe_link.click()

        # Check for input field
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Name:'.lower(), body.text.lower())

        # Input cafe name
        category_field = self.browser.find_element_by_name('name')
        category_field.send_keys("Cafe Test")

        # Create cafe owner
        self.user = User.objects.create_user(username='test_owner', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=True)

        # Input cafe owner
        category_field = self.browser.find_element_by_name('owner')
        category_field.send_keys("test_owner")
        # input price-point
        category_field = self.browser.find_element_by_name('pricepoint')
        category_field.send_keys(1)
        # save cafe
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

    def test_can_create_new_review_via_admin_page(self):
        # Access admin page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('admin:index'))

        # Check if it displays admin message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # login to admin page
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # check the Site Administration page exists
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # Check if is there link to Reviews and click it.
        cafe_link = self.browser.find_elements_by_partial_link_text('Rev')
        self.assertEquals(len(cafe_link), 1)
        cafe_link[0].click()

        # it's empty, so check for the empty message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 rev', body.text.lower())

        # Add a review by clicking on 'Add review'
        new_review_link = self.browser.find_element_by_class_name('addlink')
        new_review_link.click()

        # Check for input field
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Cafe:'.lower(), body.text.lower())

        # Create cafe user
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=False)
        # Create cafe owner
        self.owner = User.objects.create_user(username='test_owner', password='12345')
        self.owner_profile = UserProfile.objects.create(user=self.owner, is_owner=True)
        # create cafe
        cafe = Cafe(owner=self.owner_profile, name='Cafe One', pricepoint=2)
        cafe.save()

        # Input cafe name
        category_field = self.browser.find_element_by_name('cafe')
        category_field.send_keys("Cafe One")
        # Input cafe owner
        category_field = self.browser.find_element_by_name('user')
        category_field.send_keys("test_user")
        # input price-point
        category_field = self.browser.find_element_by_name('comments')
        category_field.send_keys('Excellent cafe.')
        # save cafe
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()


class PopulationScriptTest(TestCase):
    def test_population_script_changes_database(self):
        # Populate database
        populate_cafe.populate()

        # Check if the cafe has correct owner and pricepoint
        cafe = Cafe.objects.get(name='Free Spirit')
        self.assertEquals(cafe.owner.user.username, "xeniaskotti")
        self.assertEquals(cafe.pricepoint, 1)

        # Check if the cafe has correct owner and pricepoint
        cafe = Cafe.objects.get(name='CoffeeRiver')
        self.assertEquals(cafe.owner.user.username, "xeniaskotti")
        self.assertEquals(cafe.pricepoint, 2)

        # Check if the cafe has correct owner and pricepoint
        cafe = Cafe.objects.get(name='Starbucks')
        self.assertEquals(cafe.owner.user.username, "alisonscott")
        self.assertEquals(cafe.pricepoint, 3)

        # Check if the cafe has correct owner and pricepoint
        cafe = Cafe.objects.get(name='Monza')
        self.assertEquals(cafe.owner.user.username, "alisonscott")
        self.assertEquals(cafe.pricepoint, 1)

        # Check if the cafe has correct owner and pricepoint
        cafe = Cafe.objects.get(name='Fika')
        self.assertEquals(cafe.owner.user.username, "jonathan23")
        self.assertEquals(cafe.pricepoint, 2)


class ViewTest(TestCase):
    # TODO: test views
    def test_base_template_exists(self):
        # Check base.html exists inside template folder
        path_to_base = settings.TEMPLATE_DIR + '/cafe/base.html'
        print(path_to_base)
        self.assertTrue(os.path.isfile(path_to_base))

    def test_home_using_template(self):
        response = self.client.get(reverse('home'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/home.html')

    def test_about_using_template(self):
        response = self.client.get(reverse('about'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/about.html')

    def test_cafes_using_template(self):
        response = self.client.get(reverse('cafes'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/cafes.html')

    def test_login_using_template(self):
        response = self.client.get(reverse('login'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/login.html')

    def test_sign_up_using_template(self):
        response = self.client.get(reverse('sign_up'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/sign_up.html')

    def test_chosen_cafe_using_template(self):
        populate_cafe.populate()
        response = self.client.get(reverse('chosen_cafe', kwargs={'cafe_name_slug': 'monza'}))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/chosen_cafe.html')

    def test_my_account_using_template(self):
        # create test user
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=False)
        # login as test user
        self.client.login(username='test_user', password='12345')

        response = self.client.get(reverse('my_account'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/my_account.html')

    def test_add_cafe_using_template(self):
        response = self.client.get(reverse('add_cafe'))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/upload_cafe.html')

    def test_write_review_using_template(self):
        populate_cafe.populate()
        # create test owner
        self.user = User.objects.create_user(username='test_owner', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=False)
        # login as test owner
        self.client.login(username='test_owner', password='12345')

        response = self.client.get(reverse('write_review', kwargs={'cafe_name_slug': 'monza'}))
        # Check the template used to render page
        self.assertTemplateUsed(response, 'cafe/write_review.html')


class TemplateTest(TestCase):
    def test_home_shows_search_bar(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<input class="searchButton" type="submit" value="Search"/>', html=True)

    def test_home_shows_log_in_when_not_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, """<button onclick="window.location.href = '/cafe/login/';">Log In</button>""", html=True)

    def test_home_shows_log_out_when_logged_in(self):
        # create test user
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, is_owner=False)
        # login as test user
        self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse("home"))
        self.assertContains(response, """<button onclick="window.location.href = '/cafe/logout/';">Log out</button>""", html=True)

    def test_cafes_shows_name_in_template(self):
        populate_cafe.populate()
        # get all Cafes
        cafes = Cafe.objects.all()
        for cafe in cafes:
            response = self.client.get(reverse("chosen_cafe", kwargs={'cafe_name_slug': cafe.slug}))
            self.assertContains(response, '<h2>{}</h2>'.format(cafe.name), html=True)

    def test_home_shows_sign_up_when_not_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, """<button onclick="window.location.href = '/cafe/sign_up/';">Sign Up</button>""", html=True)


