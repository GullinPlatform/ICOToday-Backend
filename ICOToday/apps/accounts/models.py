from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AccountManager(BaseUserManager):
	use_in_migrations = True

	def _create_account(self, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not extra_fields.get('email') and not extra_fields.get('username') and not extra_fields.get('phone'):
			raise ValueError('The email/username/phone must be set')

		# if extra_fields.get('email'):
		# 	email = self.normalize_email(extra_fields.get('email'))
		#
		# email = self.normalize_email(email)
		account = self.model(**extra_fields)
		account.set_password(password)
		account.save()
		return account

	def create_user(self, password=None, **extra_fields):
		extra_fields['is_superuser'] = False
		extra_fields['is_staff'] = False
		return self._create_account(password, **extra_fields)

	def create_superuser(self, password, **extra_fields):
		extra_fields['is_superuser'] = True
		extra_fields['is_staff'] = True
		return self._create_account(password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
	TYPE_CHOICES = (
		(0, '需求方'),
		(1, '技术提供方')
	)
	VERIFY_PROCESS = (
		(0, '未通过'),
		(1, '审核中'),
		(2, '通过')
	)
	# Auth
	email = models.EmailField(unique=True, null=True)
	username = models.CharField(max_length=40, unique=True, null=True)
	phone = models.CharField(max_length=20, unique=True, null=True)
	# Account Info
	alias = models.CharField(max_length=20, null=True)
	avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
	type = models.IntegerField(choices=TYPE_CHOICES, default=0)

	first_name = models.CharField(max_length=40, null=True, blank=True)
	last_name = models.CharField(max_length=40, null=True, blank=True)
	# Permission
	# From inherit
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	# self-defined
	is_activated = models.BooleanField(default=False)
	is_verified = models.IntegerField(choices=VERIFY_PROCESS, default=0)
	is_company = models.BooleanField(default=False)
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	# Relations
	objects = AccountManager()
	# Settings
	USERNAME_FIELD = 'username'

	class Meta:
		ordering = ['created']

	def __str__(self):
		return self.username

	@property
	def full_name(self):
		return self.username

	@property
	def is_admin(self):
		return self.is_staff

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def get_short_name(self):
		return self.username

	def get_full_name(self):
		return self.username


class VerifyToken(models.Model):
	email = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	token = models.CharField(max_length=200)
	expire_time = models.DateTimeField(auto_now_add=True)

	@property
	def is_expired(self):
		return (timezone.now() - timedelta(hours=5)) > self.expire_time


class AccountVerifyInfo(models.Model):
	LEGAL_ID_TYPE = (
		(0, '中华人民共和国身份证'),
		(1, '护照'),
		(2, '驾照'),
	)
	account = models.OneToOneField('Account', related_name='verify_info')

	# for individual
	real_name = models.CharField(max_length=20, null=True)
	birthday = models.DateField(null=True)
	working_at = models.CharField(max_length=50, null=True)
	legal_id = models.FileField(upload_to='user_legal_id')
	legal_id_type = models.IntegerField(choices=LEGAL_ID_TYPE, null=True)
	wechat = models.CharField(max_length=50, null=True)
	qq = models.CharField(max_length=50, null=True)
	phone = models.CharField(max_length=50, null=True)
	# for company
	company_name = models.CharField(max_length=20, null=True)
	company_register_file = models.FileField(upload_to='company_register_file')
	company_phone = models.CharField(max_length=50, null=True)
	company_contact = models.CharField(max_length=50, null=True)
	company_email = models.CharField(max_length=50, null=True)
	company_address = models.CharField(max_length=50, null=True)
	company_field = models.CharField(max_length=50, null=True)
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)