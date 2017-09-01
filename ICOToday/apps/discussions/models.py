from django.db import models


class Discussion(models.Model):
	question = models.ForeignKey('posts.Post', related_name='discussions')
	account = models.ForeignKey('accounts.Account', related_name='discussions')
	title = models.CharField(max_length=200)
	content = models.TextField()
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class Reply(models.Model):
	question = models.ForeignKey('Discussion', related_name='replies')
	account = models.ForeignKey('accounts.Account', related_name='replies')
	content = models.TextField()
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question.title
