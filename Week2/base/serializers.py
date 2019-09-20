from rest_framework import serializers
from base.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'address', 'web_site')

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user
