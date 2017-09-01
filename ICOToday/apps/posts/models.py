from django.db import models


class Post(models.Model):
	STATUS_CHOICES = (
		(0, 'Processing'),
		(1, 'Verified'),
		(2, 'Completed'),
		(3, 'Promoting'),
	)
	creator = models.ForeignKey('accounts.Account', related_name='created_posts')
	appliers = models.ManyToManyField('accounts.Account', blank=True, related_name='applied_posts')
	marked = models.ManyToManyField('accounts.Account', blank=True, related_name='marked_posts')

	title = models.CharField(max_length=200)
	description_short = models.TextField()
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)

	tags = models.ManyToManyField('PostTag', related_name='posts')

	promote_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
	logo_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)

	# ICO fields
	website = models.CharField(max_length=100, null=True, blank=True)
	start_date = models.DateTimeField(null=True)
	end_date = models.DateTimeField(null=True)
	white_paper = models.FileField(upload_to='white_papers/', null=True, blank=True)
	up_votes = models.IntegerField(default=0)
	down_votes = models.IntegerField(default=0)
	video_link = models.CharField(max_length=100, null=True, blank=True)
	team_members = models.ManyToManyField('accounts.Account', blank=True, related_name='posts')

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# relation
	# fields
	# files

	def __str__(self):
		return self.title if self.title else ' '

	def num_votes(self):
		return self.up_votes - self.down_votes


class CommentsField(models.Model):
	post = models.ForeignKey('posts.Post', related_name='comments')
	author = models.ForeignKey('accounts.Account', related_name='author_questions')
	comment = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)



class PostTag(models.Model):
	TYPE_CHOICE = (
		(0, 'Industry'), (1, 'Tech')
	)
	tag = models.CharField(max_length=40)

	def __str__(self):
		return self.tag if self.tag else ' '
