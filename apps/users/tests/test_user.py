from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from django.contrib.auth import get_user_model
from django.urls import reverse

def create_user(**kwargs):
    """Helper function to create user"""
    return get_user_model().objects.create_user(**kwargs)

class UserTest(TenantTestCase):
    """Test user model and view"""

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
    
    def test_create_user(self):
        """Test creating user via view"""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Test123!',
            'password2': 'Test123!',
        }
        res = self.client.post(reverse('register'), payload, follow=True)
        redirected_path = res.request.get('PATH_INFO')
        # If form is correct, check if redirect to login page
        self.assertEquals(redirected_path, reverse('login'))
    
    def test_create_user_with_wrong_password(self):
        """Test creating user with wrong password"""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Test123!',
            'password2': 'Test123',
        }
        res = self.client.post(reverse('register'), payload, follow=True)
        redirected_path = res.request.get('PATH_INFO')
        # If it fails, will redirect to register page
        self.assertEquals(redirected_path, reverse('register'))

    def test_password_is_hashed(self):
        """Test if password is hashed after user creation"""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Test123!',
            'password2': 'Test123!',
        }
        self.client.post(reverse('register'), payload)
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('Test123!'))
    
    def test_email_already_exists(self):
        """Test creating user with existing email"""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Test123!',
            'password2': 'Test123!',
        }
        self.client.post(reverse('register'), payload)

        # Create second payload with same email
        payload2 = payload.copy()
        payload2['username'] = 'testuser2'
        res = self.client.post(reverse('register'), payload2)

        redirected_path = res.request.get('PATH_INFO')
        # If email already exists, will redirect to register page
        self.assertEquals(redirected_path, reverse('register'))



