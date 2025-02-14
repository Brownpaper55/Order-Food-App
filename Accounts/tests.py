from django.test import TestCase
from django.urls import reverse
from .models import Customer

# Create your tests here.
class CustomerRegistrationView(TestCase):
    def setUp(self):
        #set up data if needed
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'firstname':'john',
            'lastname':'Cena',
            'email': 'cena@example.com',
            'password1':'test123',
            'password2': 'test123',
            'phone':'0240395925',
        }

    def test_post_data(self):
        #test if the post successfully registers a user
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Customer.objects.filter(username='testuser').exists())


class LoginViewTests(TestCase):
    #Create a user for testing
    def setUp(self):
        self.customer = Customer.objects.create(username='client', password='password123')
        self.login_url = reverse('login')

    def test_login(self):
    #test successful login
        response = self.client.post(self.login_url,{
            'username': 'client',
            'password': 'password123'
        })
        self.assertEqual =(response.status_code, 200)
        self.assertRedirects(response, reverse('home/'))