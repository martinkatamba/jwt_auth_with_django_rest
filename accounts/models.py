from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from  .options import *
import random
import string
# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email,  password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)

        # Generate a random password if not provided
        if password =="password":
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(password)

        user.set_password(password)
        user.save(using=self._db)

        return user

    
    def create_superuser(self, email,  password,**extra_fields):
        user = self.create_user(email=email, password=password,**extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)



class UserProfile(AbstractBaseUser, PermissionsMixin):
   
    email = models.EmailField(max_length=255, unique=True)
    phone_number =models.CharField(max_length=300)
    first_name =models.CharField(max_length=300)
    last_name =models.CharField(max_length=300)
    country = models.CharField(max_length=300, choices=COUNTRY_LIST)  
  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at= models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number']

    def __str__(self):
        return self.email