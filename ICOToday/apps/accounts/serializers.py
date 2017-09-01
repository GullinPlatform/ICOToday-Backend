from rest_framework import serializers

from .models import Account, Team


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		exclude = ('user_permissions', 'groups', 'is_superuser', 'is_staff',
		           'is_active')
		read_only_fields = ('created', 'updated',)
		write_only_fields = ('password',)

	def create(self, validated_data):
		if 'phone' in validated_data:
			account = Account(phone=validated_data['phone'], username=validated_data['username'], type=validated_data['type'])
			account.set_password(validated_data['password'])
			account.save()
			return account
		elif 'email' in validated_data:
			account = Account(email=validated_data['email'], username=validated_data['username'], type=validated_data['type'])
			account.set_password(validated_data['password'])
			account.save()
			return account
		else:
			return False


class MiniAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['id', 'email', 'phone', 'avatar', 'type',
		          'first_name', 'last_name', 'linkedin', 'twitter', 'slack', 'telegram']


class TeamSerializer(serializers.ModelSerializer):
	members = MiniAccountSerializer(allow_null=True, many=True)

	class Meta:
		model = Team
		fields = ['id', 'name', 'description', 'members']
		read_only_fields = ('created', 'updated',)


class BasicTeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ['id', 'name', 'description']
		read_only_fields = ('created', 'updated',)


class BasicAccountSerializer(serializers.ModelSerializer):
	team = BasicTeamSerializer(allow_null=True)

	class Meta:
		model = Account
		fields = ['id', 'email', 'phone', 'avatar', 'type',
		          'first_name', 'last_name', 'description',
		          'team', 'linkedin', 'twitter', 'slack', 'telegram']
