from rest_framework import serializers
from base.models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

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

    creator= serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        # fields = ('id', 'name', 'creator_id', 'description', 'creator')
        fields = '__all__'


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


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # block = serializers.PrimaryKeyRelatedField(required=True, queryset=Block.objects.all())
    # creator = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # executor = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = '__all__'


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

    # block = serializers.PrimaryKeyRelatedField(required=True, queryset=Block.objects.all())
    # creator = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # executor = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = TaskComment
        fields = '__all__'
