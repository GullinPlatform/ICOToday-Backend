# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from datetime import timedelta
from django.utils import timezone
from ..accounts.models import Account, VerifyToken


def _generator(only_digit=False):
	if only_digit:
		return ''.join([random.choice(string.digits) for n in xrange(6)])
	else:
		return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])


class VerifyTokenUtils():
	@staticmethod
	def generate_token_by_user(user=None, only_digit=False):
		if not user:
			return False

		token_instance, created = VerifyToken.objects.get_or_create(account_id=user.id)
		token_instance.token = _generator(only_digit=only_digit)
		token_instance.expire_time = timezone.now() + timedelta(days=1)
		token_instance.save()
		return token_instance

	@staticmethod
	def generate_token_by_email(email=None, only_digit=False):
		user = Account.objects.filter(email=email).first()
		if not user:
			return False

		token_instance, created = VerifyToken.objects.get_or_create(account_id=user.id)
		token_instance.token = _generator(only_digit=only_digit)
		token_instance.expire_time = timezone.now() + timedelta(days=1)
		token_instance.save()
		return token_instance

	@staticmethod
	def get_token_by_user(user=None):
		if not user:
			return False
		token_instance = VerifyToken.objects.filter(account_id=user.id).first()
		return token_instance

	@staticmethod
	def get_token_by_token(token=None):
		if not token:
			return False
		token_instance = VerifyToken.objects.filter(token=token).first()
		return token_instance

	@staticmethod
	def validate_token(token_instance=None):
		if not token_instance:
			return False
		elif token_instance.is_expired:
			token_instance.token = ''
			token_instance.save()
			return False
		elif not token_instance.token:
			token_instance.expire_time = timezone.now() - timedelta(days=10)
			token_instance.save()
		else:
			return token_instance

	@staticmethod
	def expire_token(token_instance=None):
		if not token_instance:
			return False
		token_instance.expire_time = timezone.now() - timedelta(days=10)
		token_instance.token = ''
		token_instance.save()
		return token_instance

	@staticmethod
	def refresh_token(token_instance=None):
		if not token_instance:
			return False
		token_instance.expire_time = timezone.now() + timedelta(days=1)
		token_instance.token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
		token_instance.save()
		return token_instance
