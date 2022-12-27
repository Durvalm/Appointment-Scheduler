from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from django.contrib.auth import get_user_model
from django.urls import reverse

def create_user(email):
    """Helper function to create user"""
    user = get_user_model().objects.create_user(
        username='testuser',
        email=email,
        password='Test123!',
    )
    return user

# Create your tests here.
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
        user = create_user('test@example.com')
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

    def test_normalize_email(self):
        """Test email is normalized"""
        user = create_user('test@EXAMPLE.COM')
        # Check if email is normalized
        self.assertEquals(user.email, 'test@example.com')
    
    def test_password_exists(self):
        """Test password is required"""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '',
            'password2': '',
        }
        res = self.client.post(reverse('register'), payload)

        redirected_path = res.request.get('PATH_INFO')
        # If password is empty, will redirect to register pagevaloreperfumes
        self.assertEquals(redirected_path, reverse('register'))

    def test_login_user(self):
        """Test login user"""
        user = create_user('test@example.com')
        res = self.client.login(email=user.email, password='Test123!')
        self.assertEquals(res, True)
    
    def test_logout(self):
        """Test logout user"""
        user = create_user('test@example.com')

        self.client.login(email=user.email, password='Test123!')

        res = self.client.get(reverse('logout'))
        self.assertEquals(res.status_code, 302)
    
    def test_login_with_wrong_password(self):
        """Test login with wrong password"""
        user = create_user('test@example.com')
        res = self.client.login(email=user.email, password='Wrong Password')
        self.assertEquals(res, False)
    
    def test_edit_email_and_username(self):
        # Create user and force login (Authenticate)
        user = create_user('test@example.com')
        self.client.force_login(user)

        # Change email/username
        payload = {'email': 'test2@example.com', 'username': 'testuser2'}
        self.client.post(reverse('edit-profile'), payload)
        
        # Test if email/username is changed
        new_user = get_user_model().objects.get(id=user.id)
        self.assertEquals(new_user.email, 'test2@example.com')
    
    def test_edit_email_already_exists(self):
        # Create user and force login (Authenticate)
        user = create_user('test@example.com')
        create_user('existing_user@example.com')

        self.client.force_login(user)

        # Change email/username to existing email
        payload = {'email': 'existing_user@example.com', 'username': 'testuser2'}
        self.client.post(reverse('edit-profile'), payload)
        
        # Check if email is not changed
        new_user = get_user_model().objects.get(id=user.id)
        self.assertEquals(new_user.email, user.email)

    def test_edit_username(self):
        user = create_user('test@example.com')
        self.client.force_login(user)

        # Change username
        payload = {'email': 'test@example.com', 'username': 'testuser2'}
        self.client.post(reverse('edit-profile'), payload)

        # Test if username is changed and email is the same
        new_user = get_user_model().objects.get(id=user.id)
        self.assertEquals(new_user.username, 'testuser2')
        self.assertEquals(new_user.email, 'test@example.com')


    







