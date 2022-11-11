from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """Methods to create users"""

    def create_barber(self, username, email, password=None):
        """Create regular user (customer)"""
        #  Raise error if user didn't provide an email
        if not email:
            raise ValueError('User must have an email address')

        # fill up user fields with input given
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_barber=True,
            is_active=True
        )
        # Set password, save, and return user
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **kwargs):
        """Create regular user (customer)"""
        #  Raise error if user didn't provide an email
        if not email:
            raise ValueError('User must have an email address')

        # fill up user fields with input given
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=True,
        )

        # Set password, save, and return user
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        """Create superuser"""
        # fill up user fields with input given
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        # Set permissions
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        # Save and return user
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model for all users (Barbers, Admins, Superadmins, Customers...)"""
    # Credentials
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)

    # Other info
    saloon = models.ForeignKey('saloons.Saloon', on_delete=models.CASCADE, null=True)
    total_spent = models.FloatField(null=True)

    # User Role
    is_staff = models.BooleanField(default=False)
    is_barber = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Date related
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self):
        """Returns email as a string"""
        return self.email

    # Deal with permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class Admin(models.Model):
    """User model for admin"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    host_email = models.EmailField(max_length=255, unique=True)
    host_passcode = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email


