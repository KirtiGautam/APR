from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from datetime import date


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('admin', True)
        extra_fields.setdefault('user_type', 'Staff')
        return self._create_user(email, password, **extra_fields)

    def create_staff(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', 'Staff')
        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('user_type', 'Staff')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    admin = models.BooleanField(default=False)
    status_choices = (
        ('A', 'Active'),
        ('P', 'Pending'),
        ('R', 'Rejected'),
    )
    status = models.CharField(
        max_length=2, choices=status_choices, default='A')
    is_staff = models.BooleanField(default=False)
    user_choices = (
        ('Parent', 'Parent'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
    )
    user_type = models.CharField(
        choices=user_choices, max_length=10, default='Student')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def unreads(self):
        return self.Recipient.filter(Read=False).count()


class Class(models.Model):
    name = models.CharField(max_length=15, unique=True)


class Student(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name='Student')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    Pincode = models.PositiveIntegerField()
    Contact = models.CharField(max_length=15)
    Class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='Students')


class Teacher(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name='Teacher')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    ROLE_CHOICES = (
        ('C', 'Class Teacher'),
        ('S', 'Subject Teacher'),
        ('P', 'Principal'),
        ('I', 'Incharge'),
        ('N', 'Non-Academic Staff'),
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    District = models.CharField(max_length=255)
    Pincode = models.PositiveIntegerField()
    Contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.__str__


class video(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    Local = models.BooleanField(default=True)
    file = models.FileField(upload_to='videos/', default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name


class pdf(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    file = models.FileField(upload_to='pdfs/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name
