#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AccountInfo(models.Model):
	# Account Info
	avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

	first_name = models.CharField(max_length=40, null=True, blank=True)
	last_name = models.CharField(max_length=40, null=True, blank=True)

	title = models.CharField(max_length=40, null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	team = models.ForeignKey('Team', related_name='members', null=True, blank=True)

	# Social Media
	linkedin = models.CharField(max_length=100, null=True, blank=True)
	twitter = models.CharField(max_length=100, null=True, blank=True)
	slack = models.CharField(max_length=100, null=True, blank=True)
	telegram = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name


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
		account.info = info
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
		(0, 'ICO Company'),
		(1, 'ICO Investor')
	)

	VERIFY_PROCESS = (
		(0, 'Not Passed'),
		(1, 'Passed'),
		(2, 'Verifying')
	)

	# Auth
	email = models.EmailField(unique=True, null=True, blank=True)
	phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
	type = models.IntegerField(choices=TYPE_CHOICES, default=0)

	# Info
	info = models.OneToOneField('AccountInfo', related_name='account')

	# Permission
	# # from inherit
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	# # self defined
	is_activated = models.BooleanField(default=False)
	is_verified = models.IntegerField(choices=VERIFY_PROCESS, default=0)

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
	email = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	token = models.CharField(max_length=200)
	expire_time = models.DateTimeField(auto_now_add=True)

	@property
	def is_expired(self):
		return (timezone.now() - timedelta(hours=5)) > self.expire_time


class Team(models.Model):
	# Team Info
	name = models.CharField(max_length=50, null=True)
	description = models.TextField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
