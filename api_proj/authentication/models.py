# from django.db import models
# import jwt
# from datetime import timedelta
# from django.core import validators
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import BaseUserManager
# from datetime import datetime
# from django.conf import settings
# import uuid
# from django.utils import timezone

# class MyUserManager(BaseUserManager):

#     def _create_user(self, username, email, password=None, **extra_fields):
#         if not username:
#             raise ValueError('Need username field!')

#         if not email:
#             raise ValueError('Need email field!')

#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_user(self, username, email, password=None, **extra_fields):

#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)

#         return self._create_user(username, email, password, **extra_fields)

#     def create_superuser(self, username, email, password, **extra_fields):

#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(username, email, password, **extra_fields)

# class MyUser(AbstractBaseUser, PermissionsMixin):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     username = models.CharField(db_index=True, max_length=255, unique=True)

#     email = models.EmailField(
#         validators=[validators.validate_email],
#         unique=True,
#         blank=False
#         )

#     last_login = models.DateTimeField(auto_now_add=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     first_name = models.CharField(max_length=20)
#     last_name  = models.CharField(max_length=20)
#     is_staff = models.BooleanField(default=False)

#     is_active = models.BooleanField(default=True)

#     USERNAME_FIELD = 'email'

#     REQUIRED_FIELDS = ('username',)

#     objects = MyUserManager()

#     def __str__(self):

#         return self.username

#     @property
#     def token(self):

#         return self._generate_jwt_token()

#     def get_full_name(self):

#         return self.username

#     def get_short_name(self):

#         return self.username

#     def _generate_jwt_token(self):
 
#         dt = datetime.now() + timedelta(days=60)

#         token = jwt.encode({
#             'id': self.pk,
#             'exp': int(dt.strftime('%s'))
#         }, settings.SECRET_KEY, algorithm='HS256')

#         return token.decode('utf-8')








