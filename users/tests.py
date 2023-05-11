from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 


""" 
Tests for user api
"""
CREATE_USER_URL = reverse('users:create') #the url that handles the creating of users

#a helper function to create the users with passed-in parameters
def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITests(TestCase):
    """Tests The Public features of the User API(e.g user registration)"""
    def setUp(self):
        self.client = APIClient()

    #sends the payload to the url then asserts the response
    def test_create_user_success(self):
        payload ={

            'email':'test@example.com',
            'password':'pass123',
            'name' :'Test Name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEquals(res.status_code,status.HTTP_201_CREATED)
        user= get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
    
    def test_user_with_email_exists_error(self):
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name' :'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        payload = {
            'email':'test@example.com',
            'password':'ps',
            'name':'Test Name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)
