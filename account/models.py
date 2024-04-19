from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid 


# class MyAccountManager(BaseUserManager):
#     def create_user(self, email, phone, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         # if not username:
#         #     raise ValueError('Users must have a username')

#         user = self.model(
#             email=self.normalize_email(email),
#             # username=username,
#             password=password,
#             phone=phone,
            
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

    
#     # use_in_migrations = True

#     # def _create_user(self, email, password, **extra_fields):
#     #     """Create and save a User with the given email and password."""
#     #     if not email:
#     #         raise ValueError('The given email must be set')
#     #     email = self.normalize_email(email)
#     #     user = self.model(email=email, **extra_fields)
#     #     user.set_password(password)
#     #     user.save(using=self._db)
#     #     return user

#     def create_user(self, email, password=None, **extra_fields):
#         """Create and save a regular User with the given email and password."""
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         extra_fields.setdefault('is_admin', False)
#         return self._create_user(email, password, **extra_fields)
    

#     # def create_superuser(self, email,phone, password):
#     #     user = self.create_user(
#     #         email=self.normalize_email(email),
#     #         password=password,
#     #         phone=phone,
#     #         # username=username,
#     #     )
#     #     user.is_admin = True
#     #     user.is_staff = True
#     #     user.is_superuser = True
#     #     user.role = 'admin'
#     #     user.save(using=self._db)
        
#     #     return user
#     def create_superuser(self, email, phone, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             phone=phone,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.role = 'admin'
#         user.save(using=self._db)
        
#         return user
class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone, password, **extra_fields):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60,default=email)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False,null=True,blank=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)
    is_superuser = models.BooleanField(default=False,null=True,blank=True)
    full_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    # address = models.CharField(max_length=140,null=True,blank=True)
    dob = models.CharField(max_length=30,null=True,blank=True)
    role = models.CharField(max_length=30,null=True,blank=True,default="student")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone',]


    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin
        
    def has_module_perms(self,app_label):
        return True

    # class Meta:
    #     ordering = ('-email',)
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)      


# ===========================================================================

# from django.db import models
# import uuid 
# from django.contrib.auth.models import User

class OtpVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10, null=True,blank=True)
    count = models.IntegerField(default=5)


    class Meta:
        db_table = 'otp_verification'
    def __str__(self):
        return self.otp
        