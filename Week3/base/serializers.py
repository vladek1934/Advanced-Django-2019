from rest_framework import serializers
from base.models import *


# make profile creation via signal
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'address', 'web_site', 'avatar')

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile


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

        return user


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    # project = serializers.PrimaryKeyRelatedField(required=True, queryset=Project.objects.all())

    class Meta:
        model = Project_member
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

# class Task_document(models.Model):
#     document = models.FileField()
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#
#
# class Task_comment(models.Model):
#     body = models.TextField()
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
