# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string


def random_string():
	return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])


def _filename(instance, filename, _prefix):
	_post_fix = random_string()
	_instance_id = instance.id
	filename = filename.lower()
	file_name = filename.split('.')[0][:5]
	file_extension = filename.split('.')[-1]

	return '%s/%s/%s.%s.%s' % (_instance_id, _prefix, file_name, _post_fix, file_extension)


def company_icon_upload(instance, filename):
	return 'company/' + _filename(instance, filename, r'icon')


def company_certificate_upload(instance, filename):
	return 'company/' + _filename(instance, filename, r'certificate')


def user_avatar_upload(instance, filename):
	return 'user/' + _filename(instance, filename, r'avatar')


def project_icon_upload(instance, filename):
	return 'project/' + _filename(instance, filename, r'icon')


def project_promo_upload(instance, filename):
	return 'project/' + _filename(instance, filename, r'promo_icon')
