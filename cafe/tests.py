from django.test import TestCase
from cafe.models import *


# Create your tests here.
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

    def test_str_representation(self):
        # create test cafe
        cafe = Cafe(owner=self.user_profile, name='Cafe One', pricepoint=2)
        cafe.save()
        # check if the __str__ method return the cafe's name
        self.assertEqual(str(cafe), cafe.name)

    def tearDown(self):
        self.user.delete()
