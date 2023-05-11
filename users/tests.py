from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 


""" 
Tests for user api
"""
CREATE_USER_URL = reverse('users:create') #the url that handles the creating of users
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')

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

    def test_create_token_for_user(self):
        user_details ={
            'name':'Test Name',
            'email':'test@example.com',
            'password':'testpass123'
       }
        create_user(**user_details)
        payload ={
            'email':user_details['email'],
            'password':user_details['password'],

        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    
    def test_create_token_blank_password_error(self):
        payload = {'email':'test@example','password':''}
        res = self.client.post(TOKEN_URL,payload=payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_bad_credentials_error(self):
        create_user(name='testname',email='test@example.com',password='testpassword')
        payload ={
            'email': 'test@example.com',
            'password': 'badpassword',
        }
        res =self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Tests that require User to be authenticated"""
    def setUp(self):
        self.user =create_user(
            email='test@example.com',
            password ='testpass123',
            name ='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.asserEqual(res.data,{
            'name':self.user.name,
            'email' : self.user.email
        })

    def test_post_not_allowed(self):
        res = self.client.post(ME_URL,{})
        self.asserEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        payload = {
            'name':'updated_name',
            'password':'newpassword'
        }
        res = self.client.patch(ME_URL,payload)
        self.user.refresh_db()
        self.assertEqual(self.user.name,payload['name'])
        self.assertEqual(self.user.name,payload['password'])
        self.assertEqual(res.status_code,status.HTTP_200_OK)
