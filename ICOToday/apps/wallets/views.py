# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Wallet

from .serializers import WalletSerializer


class WalletViewSet(viewsets.ViewSet):
	queryset = Wallet.objects.all()
	permission_classes = (IsAuthenticated,)

	def retrieve(self, request):
		try:
			wallet = request.user.wallet
		except Wallet.DoesNotExist:
			wallet = Wallet.objects.create(account_id=request.user.id)

		serializer = WalletSerializer(wallet)
		return Response(serializer.data, status=status.HTTP_200_OK)
