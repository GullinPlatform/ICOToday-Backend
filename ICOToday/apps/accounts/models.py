# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from ..utils.upload_filename import user_avatar_upload


class AccountInfo(models.Model):
	TYPE_CHOICES = (
		(-1, 'Not Choose'),
		(0, 'Company'),
		(1, 'Investor'),
		(2, 'Expert'),
		(3, 'Advisor'),
	)
	# Account Type
	type = models.IntegerField(choices=TYPE_CHOICES, default=-1)

	# Personal Info
	avatar = models.ImageField(upload_to=user_avatar_upload, default='avatars/default.jpg', null=True, blank=True)
	first_name = models.CharField(max_length=40, null=True, blank=True)
	last_name = models.CharField(max_length=40, null=True, blank=True)
	title = models.CharField(max_length=40, null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	# Is Verified
	is_verified = models.BooleanField(default=False)

	# My Company
	company = models.ForeignKey('companies.Company', related_name='members', null=True, blank=True)
	company_admin = models.ForeignKey('companies.Company', related_name='admins', null=True, blank=True)
	company_pending = models.ForeignKey('companies.Company', related_name='pending_members', null=True, blank=True)

	# Interested Fields
	interests = models.ManyToManyField('projects.ProjectTag', related_name='interests', blank=True)

	# Social Media
	linkedin = models.CharField(max_length=100, null=True, blank=True)
	twitter = models.CharField(max_length=100, null=True, blank=True)
	telegram = models.CharField(max_length=100, null=True, blank=True)
	facebook = models.CharField(max_length=100, null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name if self.first_name and self.last_name else str(self.id)

	def full_name(self):
		return self.first_name + ' ' + self.last_name if self.first_name and self.last_name else str(self.id)


class AccountManager(BaseUserManager):
	use_in_migrations = True

	def _create_account(self, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not extra_fields.get('email') and not extra_fields.get('phone'):
			raise ValueError('The email/phone must be set')

		info = AccountInfo.objects.create()
		account = self.model(**extra_fields)
		account.set_password(password)
		account.info_id = info.id
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
	# Auth
	email = models.EmailField(unique=True, null=True, blank=True)
	phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

	# Info
	info = models.OneToOneField('AccountInfo', related_name='account')

	# Permission
	# # from inherit
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# Relations
	objects = AccountManager()

	# Settings
	USERNAME_FIELD = 'email'

	class Meta:
		ordering = ['created']

	def __str__(self):
		return self.email

	@property
	def full_name(self):
		return self.email if self.email else self.phone

	@property
	def is_admin(self):
		return self.is_staff

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def get_short_name(self):
		return self.email

	def get_full_name(self):
		return self.email


class VerifyToken(models.Model):
	account = models.ForeignKey('Account', related_name='verify_token')
	token = models.CharField(max_length=200)
	expire_time = models.DateTimeField(auto_now_add=True)

	@property
	def is_expired(self):
		return (timezone.now() - timedelta(hours=5)) > self.expire_time


class ExpertApplication(models.Model):
	STATUS_CHOICES = (
		(0, 'Processing'),
		(1, 'Approved'),
		(2, 'Declined'),
	)

	# Info
	account = models.OneToOneField('AccountInfo', related_name='expert_application')
	detail = models.TextField()
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	response = models.TextField()

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.account.email
