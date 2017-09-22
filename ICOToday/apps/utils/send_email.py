# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(receiver_list, subject, template_name, ctx):
	email = EmailMessage(subject, render_to_string('email/%s.html' % template_name, ctx), 'no-reply@icotoday.io', receiver_list)
	email.content_subtype = 'html'
	email.send()
