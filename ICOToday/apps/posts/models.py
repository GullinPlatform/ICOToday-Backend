from django.db import models


class Post(models.Model):
	STATUS_CHOICES = (
		(0, 'Processing'),
		(1, 'Verified'),
		(2, 'Completed'),
	)
	creator = models.ForeignKey('accounts.Account', related_name='created_questions')
	appliers = models.ManyToManyField('accounts.Account', related_name='applied_questions')
	marked = models.ManyToManyField('accounts.Account', related_name='marked_questions')

	title = models.CharField(max_length=200)
	description_short = models.TextField()
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	prize = models.IntegerField()
	due_date = models.DateTimeField(null=True)
	difficulty = models.IntegerField(default=1)

	industry_tags = models.ManyToManyField('QuestionTag', related_name='industry_questions')
	tech_tags = models.ManyToManyField('QuestionTag', related_name='tech_questions')

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# relation
	# fields
	# files

	def __str__(self):
		return self.title


class QuestionField(models.Model):
	question = models.ForeignKey('Post', related_name='fields')
	title = models.CharField(max_length=20)
	content = models.TextField()

	def __str__(self):
		return self.question.title + '-' + self.title


class QuestionFile(models.Model):
	question = models.ForeignKey('Post', related_name='files')
	file = models.FileField(upload_to='question_files/')
	file_name = models.CharField(max_length=40)
	file_size = models.IntegerField(default=0)

	def __str__(self):
		return self.question.title + ' file'


class QuestionTag(models.Model):
	TYPE_CHOICE = (
		(0, 'Industry'), (1, 'Tech')
	)
	tag = models.CharField(max_length=40)
	type = models.IntegerField(choices=TYPE_CHOICE)

	def __str__(self):
		return self.tag
