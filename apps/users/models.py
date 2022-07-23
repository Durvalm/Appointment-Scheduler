from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Methods to create users"""

    def create_user(self, first_name, last_name, email, password=None):
        """Create regular user (customer)"""
        #  Raise error if user didn't provide an email
        if not email:
            raise ValueError('User must have an email address')

        # fill up user fields with input given
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        # Set password, save, and return user
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password):
        """Create superuser"""
        # fill up user fields with input given
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    # User Role
    is_staff = models.BooleanField(default=False)
    is_barber = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Date related
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    # Additional Methods
    def full_name(self):
        """Gets full name"""
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """Returns email as a string"""
        return self.email

    # Deal with permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



