from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ['btc_amount', 'eth_amount', 'icc_amount', 'btc_wallet_address', 'eth_wallet_address', 'icc_wallet_address', 'created', 'updated']
		read_only_fields = ('created', 'updated',)