from rest_framework import serializers
from base.models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password', 'email',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)

        # profile = Profile.objects.create(
        #     user=user
        # )
        # profile.save()
        return user


# In future make profile creation via signal
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    parent_user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'parent_user', 'bio', 'address', 'web_site', 'avatar')

    def get_parent_user(self, obj):
        if obj.user is not None:
            return obj.user.username + " with id " + str(obj.user.id)
        return ''


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        # fields = ('id', 'name', 'creator_id', 'description', 'creator')
        fields = '__all__'

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def validate_name(self, value):
        if (len(value) >= 200 or len(value) <= 0):
            raise serializers.ValidationError('Name field must be in range 0-200 symbols')
        return value


class ProjectMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProjectMember
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Block
        fields = '__all__'


class TaskShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'executor', 'creator', 'block')

    def validate_order(self, value):
        if int(value) > 100 or int(value) < 1:
            raise serializers.ValidationError('Order field must be in range 1-100')
        return value


class TaskFullSerializer(TaskShortSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('order', 'description',)


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskDocument
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskComment
        fields = '__all__'
