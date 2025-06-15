from rest_framework import serializers
from .models import Instagram_User

class InstagramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagram_User
        fields = ['username', 'full_name', 'followers', 'posts', 'profile_pic']