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

        profile = Profile.objects.create(
            user=user
        )
        profile.save()
        return user


# In future make profile creation via signal
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    origin = serializers.SerializerMethodField()

    # user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('id', 'origin', 'bio', 'address', 'web_site', 'avatar')

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile

    def get_origin(self, obj):
        if obj.user is not None:
            return obj.user.username + " with id " + str(obj.user.id)
        return ''


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)
    # creator_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # creator = serializers.CharField(source='creator.username', read_only=True)

    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        # fields = ('id', 'name', 'creator_id', 'description', 'creator')
        fields = '__all__'

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def validate_name(self, value):
        if len(value) >= 100:
            raise serializers.ValidationError('Name field must be max len: 100')
        return value


# class ProjectSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=300)
#     description = serializers.CharField(max_length=300)
#
#     def create(self, validated_data):
#         project = Project.objects.create(**validated_data)
#         return project
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('status', instance.description)
#         instance.save()
#
#         return instance
#
#     # def validate(self, attrs):
#     #     pass
#
#     def validate_name(self, value):
#         if len(value) >= 100:
#             raise serializers.ValidationError('Name field must be max len: 100')
#         return value
#
#     def get_creator_name(self, obj):
#         if obj.creator is not None:
#             return obj.creator.username
#         return ''


class ProjectMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # project = serializers.PrimaryKeyRelatedField(required=True, queryset=Project.objects.all())

    class Meta:
        model = ProjectMember
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # project = serializers.PrimaryKeyRelatedField(required=True, queryset=Project.objects.all())

    class Meta:
        model = Block
        fields = '__all__'


class TaskShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # block = serializers.PrimaryKeyRelatedField(required=True, queryset=Block.objects.all())
    # creator = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # executor = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'executor', 'creator', 'block')

    def validate_order(self, value):
        if int(value) >= 100 or int(value) <= 20:
            raise serializers.ValidationError('Order field must be in range 20-100')
        return value



class TaskFullSerializer(TaskShortSerializer):
    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('order', 'description',)


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # block = serializers.PrimaryKeyRelatedField(required=True, queryset=Block.objects.all())
    # creator = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # executor = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = TaskDocument
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    # block = serializers.PrimaryKeyRelatedField(required=True, queryset=Block.objects.all())
    # creator = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # executor = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = TaskComment
        fields = '__all__'
