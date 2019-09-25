from django.core.files.storage import FileSystemStorage
from django.db import models
from Images import *
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from base.ChoiceFields import STATUS_CHOICES
from django.utils import timezone
from rest_framework.authtoken.models import Token


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default='none')
    address = models.CharField(max_length=300, default='none')
    web_site = models.CharField(max_length=300, default='none')
    avatar = models.FileField(default='Images/Default.png')

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description? You can add one!")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdprojects")


class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Block(models.Model):
    name = models.CharField(max_length=300)
    type = models.IntegerField(choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdtasks")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignedtasks")
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    order = models.IntegerField()


class TaskDocument(models.Model):
    document = models.FileField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskComment(models.Model):
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
