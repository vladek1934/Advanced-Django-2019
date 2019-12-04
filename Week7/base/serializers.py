from rest_framework import serializers
from base.models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('projects',)

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'address', 'web_site', 'avatar')


class ProfileNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'address', 'web_site', 'avatar')


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
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


# class TaskShortSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     block_id = serializers.IntegerField()
#     executor_id = serializers.IntegerField()
#     creator_id = serializers.IntegerField()
#
#
#     def create(self, validated_data):
#         task = Task.objects.create(**validated_data)
#         return task
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.block_id = validated_data.get('block_id', instance.block_id)
#         instance.executor_id = validated_data.get('executor_id', instance.executor_id)
#         instance.creator_id = validated_data.get('creator_id', instance.creator_id)
#         instance.save()
#         return instance

class TaskShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'executor', 'creator', 'block')


# class TaskFullSerializer(TaskShortSerializer):
#     priority = serializers.IntegerField()
#     description = serializers.CharField()
#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     def validate_priority(self, value):
#         if int(value) > 100 or int(value) < 1:
#             raise serializers.ValidationError('Priority field must be in range 1-100')
#         return value
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.block_id = validated_data.get('block_id', instance.block_id)
#         instance.description = validated_data.get('description', instance.description)
#         instance.priority = validated_data.get('priority', instance.priority)
#         instance.save()
#         return instance
#
#     def validate_priority(self, value):
#         if int(value) > 100 or int(value) < 1:
#             raise serializers.ValidationError('Priority field must be in range 1-100')
#         return value


class TaskFullSerializer(TaskShortSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('priority', 'description',)

    def validate_priority(self, value):
        if int(value) > 100 or int(value) < 1:
            raise serializers.ValidationError('Priority field must be in range 1-100')
        return value

    def validate_description(self, value):
        if len(value) >= 200 or len(value) <= 10:
            raise serializers.ValidationError('Description field must be in range 10-200 symbols')
        return value


class BlockNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tasks = TaskFullSerializer(many=True)

    class Meta:
        model = Block
        fields = '__all__'

    def create(self, validated_data):
        tasks = validated_data.pop('tasks')
        block = Block.objects.create(**validated_data)

        for task in tasks:
            task, created = task.objects.get_or_create(name=task['name'], description=task['description'],
                                                       block=block, priority=task['priority'],
                                                       creator=task['creator'], executor=['executor'])
        return block


class SubmitionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskSubmition
        fields = '__all__'

    def validate_text(self, value):
        if len(value) <= 10:
            raise serializers.ValidationError('Text field must contain more than 10 symbols')
        return value


class DocumentSerializer(SubmitionSerializer):
    class Meta(SubmitionSerializer.Meta):
        model = TaskDocument
        fields = TaskShortSerializer.Meta.fields + ('document', 'task')


class CommentSerializer(SubmitionSerializer):
    class Meta(SubmitionSerializer.Meta):
        model = TaskComment
        fields = TaskShortSerializer.Meta.fields + ('task',)
