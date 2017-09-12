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
	title = models.CharField(max_length=200)
	description_short = models.CharField(max_length=200, null=True, blank=True)
	description_full = models.TextField()
	tags = models.ManyToManyField('PostTag', related_name='posts')

	# Time
	start_datetime = models.DateTimeField(null=True)
	end_datetime = models.DateTimeField(null=True)
	timezone = models.CharField(max_length=10, default='EST')

	# ICO Details
	type = models.IntegerField(choices=TYPE_CHOICES, default=0)
	coin_name = models.CharField(max_length=100, null=True, blank=True)
	ratio = models.FloatField(default=1)
	coin_type = models.CharField(max_length=20, default='BTC')
	maximum_goal = models.IntegerField(default=0)
	minimum_goal = models.IntegerField(default=0)
	equality_on_offer = models.IntegerField(default=0)

	current = models.IntegerField(default=0)
	money_raised = models.IntegerField(default=0)

	# Supplements
	promote_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
	logo_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
	white_paper = models.FileField(upload_to='white_papers/', null=True, blank=True)
	video_link = models.CharField(max_length=100, null=True, blank=True)
	website = models.CharField(max_length=100, null=True, blank=True)

	# Platform
	rating = models.IntegerField(default=0)
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
	# fields
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
