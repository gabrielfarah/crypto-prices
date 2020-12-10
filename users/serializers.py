from rest_framework import serializers

from .models import AccountUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ('email',)
