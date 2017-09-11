from rest_framework import serializers

from .models import Account, Team, AccountInfo


class BasicTeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = ['id', 'name', 'description']
		read_only_fields = ('created', 'updated',)


class AuthAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		exclude = ('user_permissions', 'groups', 'is_superuser', 'is_staff', 'is_active', 'info')
		read_only_fields = ('created', 'updated',)
		write_only_fields = ('password',)

	def create(self, validated_data):
		if 'phone' in validated_data:
			account = Account(phone=validated_data['phone'], type=validated_data['type'])
		elif 'email' in validated_data:
			account = Account(email=validated_data['email'], type=validated_data['type'])
		else:
			return False

		account.set_password(validated_data['password'])
		info = AccountInfo.objects.create()
		account.info = info
		account.save()
		return account

	def update(self, instance, validated_data):
		instance.set_password(validated_data['password'])
		instance.save()
		return instance


class AccountInfoSerializer(serializers.ModelSerializer):
	team = BasicTeamSerializer(allow_null=True, read_only=True)

	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'first_name', 'last_name',
		          'team', 'title', 'description', 'is_advisor',
		          'linkedin', 'twitter', 'telegram', 'facebook']


class BasicAccountSerializer(serializers.ModelSerializer):
	info = AccountInfoSerializer()

	class Meta:
		model = Account
		fields = ['id', 'email', 'phone', 'type', 'is_verified', 'info']


class BasicAccountInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'first_name', 'last_name',
		          'team', 'title', 'description', 'is_advisor',
		          'linkedin', 'twitter', 'telegram', 'facebook', 'account']


class TeamSerializer(serializers.ModelSerializer):
	members = BasicAccountInfoSerializer(allow_null=True, many=True)

	class Meta:
		model = Team
		fields = ['id', 'name', 'description', 'members']
		read_only_fields = ('created', 'updated',)
