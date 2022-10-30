from pydoc import describe
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)

# User=get_user_model()
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, is_admin=False, is_active=True, is_staff=False):
        if not email:
            raise ValueError("User must have a email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj= self.model(
            email = self.normalize_email(email),
             #normalize_email it is an built-in function which allows us to use the email again and again
        )
        user_obj.set_password(password) #change user passowrd
        user_obj.staff= is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email, password=None):
        user_staff= self.create_user(
            email,
            password=password,
            is_staff=True
        )
        user_staff.save(using=self._db)
        return user_staff

    def create_superuser(self, email, password=None):
        user_admin = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        user_admin.save(using=self._db)
        return user_admin




class User(AbstractUser):
    email=models.EmailField(max_length=100,unique=True)
    active=models.BooleanField(default=True) #can login
    staff=models.BooleanField(default=True) # cannot make changes
    admin=models.BooleanField(default=True) #superuser- can make changes
    
    #USERNAME_FIELD = 'email' #username

    #USER_NAME and password are required by default
    REQUIRED_FIELDS = []

    objects= UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label='tasks'


class todo(models.Model):
    task=models.CharField("Task",max_length=100) # the first argument is the verbose name
    description=models.TextField("Describe",blank=True)
    time=models.IntegerField("Max time you will take to do it",blank=True)
    quote=models.ImageField(null=True,blank=True, upload_to='images/')
    #day=models.DateTimeField("Due Date",blank=True,null=True)

    def __str__(self):
        return self.task