#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models


class Post(models.Model):
	STATUS_CHOICES = (
		(0, 'Verifying'),
		(1, 'Verified'),
		(2, 'Completed'),
		(3, 'Promoting'),
		(4, 'Premium'),
		(5, 'Closed'),
	)

	TYPE_CHOICES = (
		(0, 'Pre-ICO'),
		(1, 'ICO'),
	)
	creator = models.ForeignKey('accounts.Account', related_name='created_posts')
	marked = models.ManyToManyField('accounts.Account', blank=True, related_name='marked_posts')
	team = models.ForeignKey('accounts.Team', blank=True, related_name='posts')

	# Information
	title = models.CharField(max_length=100)
	description_short = models.CharField(max_length=200, null=True, blank=True)
	description_full = models.TextField()
	tags = models.ManyToManyField('PostTag', related_name='posts')
	category = models.CharField(max_length=100)

	# Time
	start_datetime = models.DateTimeField(null=True, blank=True)
	end_datetime = models.DateTimeField(null=True, blank=True)

	# ICO Details
	type = models.IntegerField(choices=TYPE_CHOICES, default=0)
	coin_name = models.CharField(max_length=100, null=True, blank=True)
	ratio = models.FloatField(null=True, blank=True)
	coin_type = models.CharField(max_length=20, null=True, blank=True)
	maximum_goal = models.IntegerField(null=True, blank=True)
	minimum_goal = models.IntegerField(null=True, blank=True)
	equality_on_offer = models.FloatField(null=True, blank=True)

	current = models.IntegerField(null=True, blank=True)
	money_raised = models.IntegerField(null=True, blank=True)

	# Supplements
	promote_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
	logo_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
	white_paper = models.FileField(upload_to='white_papers/', null=True, blank=True)
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

	# relation
	# files
	class Meta:
		ordering = ['-start_datetime']

	def __str__(self):
		return self.title

	def time_passed(self):
		return True if self.end_date > timezone.now() else False


class PostTag(models.Model):
	tag = models.CharField(max_length=40)

	def __str__(self):
		return self.tag if self.tag else ' '


class RatingDetail(models.Model):
	rater = models.ForeignKey('accounts.Account', related_name='ratings')
	post = models.ForeignKey('Post', related_name='rating_detail')
	detail = models.TextField()
	score = models.IntegerField(default=0)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.post.title + ' by ' + self.rater.email


class PromotionApplication(models.Model):
	STATUS_CHOICES = (
		(0, 'Processing'),
		(1, 'Approved'),
		(2, 'Declined'),
	)

	# Info
	account = models.ForeignKey('accounts.Account', related_name='my_promotions')
	team = models.ForeignKey('accounts.Team', related_name='promotions')
	detail = models.TextField()
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	response = models.TextField()

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.team.name
