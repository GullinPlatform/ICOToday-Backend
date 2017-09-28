# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from .models import Message, Conversation


class ConversationViewSet(viewsets.ViewSet):
	queryset = Conversation.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def retrieve_latest(self, request, sender_pk):
		# last 10 conversation
		pass

	def retrieve_more(self, request, sender_pk):
		# 10 more conversation
		pass

	def start_conversation(self, request, account_info_pk):
		# if never talk with, create new conversation, else return conversation id
		# should take 2 AccountInfo id as input
		pass

	def reply(self, request, sender_pk):
		pass

	def read(self, request, sender_pk):
		pass
