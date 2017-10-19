# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.db import models

from ..utils.upload_filename import project_promo_upload, project_icon_upload


class Project(models.Model):
	"""
	AccountInfo Model
	Relations:
	field name | key type | origin model
	1) rating_details ForeignKey projects.Project
	"""
	STATUS_CHOICES = (
		(0, 'Verifying'),
		(1, 'Verified'),
		(2, 'Completed'),
		(3, 'Promoting'),
		(4, 'Premium'),
		(5, 'Closed'),
		(6, 'Rejected'),
	)

	TYPE_CHOICES = (
		(0, 'Pre-ICO'),
		(1, 'ICO'),
	)

	marked = models.ManyToManyField('accounts.AccountInfo', blank=True, related_name='marked_projects')
	company = models.OneToOneField('companies.Company', blank=True, related_name='project')

	# Information
	name = models.CharField(max_length=100, unique=True)
	description_short = models.CharField(max_length=200, null=True, blank=True)
	description_full = models.TextField()
	token_sale_plan = models.TextField(null=True, blank=True)
	tags = models.ManyToManyField('ProjectTag', related_name='posts')
	category = models.CharField(max_length=100)

	# Time
	start_datetime = models.DateTimeField(null=True, blank=True)
	end_datetime = models.DateTimeField(null=True, blank=True)

	# ICO Details
	type = models.IntegerField(choices=TYPE_CHOICES, default=0)
	coin_name = models.CharField(max_length=100, null=True, blank=True)
	coin_unit = models.CharField(max_length=20, null=True, blank=True)
	accept = models.CharField(max_length=100, null=True, blank=True)
	ratio = models.FloatField(null=True, blank=True)
	maximum_goal = models.IntegerField(null=True, blank=True)
	minimum_goal = models.IntegerField(null=True, blank=True)
	equality_on_offer = models.FloatField(null=True, blank=True)
	initial_price = models.FloatField(null=True, blank=True)

	current = models.IntegerField(null=True, blank=True)
	money_raised = models.IntegerField(null=True, blank=True)

	# Supplements
	promote_image = models.ImageField(upload_to=project_promo_upload, null=True, blank=True)
	logo_image = models.ImageField(upload_to=project_icon_upload, null=True, blank=True)
	white_paper = models.CharField(max_length=100, null=True, blank=True)
	video_link = models.CharField(max_length=100, null=True, blank=True)
	website = models.CharField(max_length=100, null=True, blank=True)

	# Platform
	rating = models.IntegerField(null=True, blank=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)

	# Social Media
	medium = models.CharField(max_length=100, null=True, blank=True)
	twitter = models.CharField(max_length=100, null=True, blank=True)
	slack = models.CharField(max_length=100, null=True, blank=True)
	telegram = models.CharField(max_length=100, null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['start_datetime']

	def __str__(self):
		return self.name

	def time_passed(self):
		if not self.end_datetime:
			return False
		return True if self.end_datetime > timezone.now() else False


class ProjectTag(models.Model):
	"""
	ProjectTag Model
	Relations:
	field name | key type | origin model
	1) accounts ManyToManyField accounts.AccountInfo
	2) posts ManyToManyField projects.Project
	"""
	tag = models.CharField(max_length=40)

	def __str__(self):
		return self.tag if self.tag else ' '


class ProjectRatingDetail(models.Model):
	rater = models.ForeignKey('accounts.AccountInfo', related_name='my_rating_details')
	score = models.IntegerField(default=0)
	content = models.TextField()

	# Relation
	project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='rating_details')

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content[:15]

	class Meta:
		ordering = ['-created']
