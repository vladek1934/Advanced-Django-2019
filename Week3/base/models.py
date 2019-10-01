from django.core.files.storage import FileSystemStorage
from django.db import models
from Images import *
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from base.ChoiceFields import STATUS_CHOICES
from django.utils import timezone
from rest_framework.authtoken.models import Token


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_login}'

    @property
    def my_projects(self):
        return self.projects

    @property
    def tasks_count(self):
        return self.assigned_tasks.count()

    def __str__(self):
        return f'{self.id}: {self.username}'


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default='none')
    address = models.CharField(max_length=300, default='none')
    web_site = models.CharField(max_length=300, default='none')
    avatar = models.FileField(default='Images/Default.png')

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description? You can add one!")
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="createdprojects")

    @property
    def block_count(self):
        return self.blocks.count()

    @property
    def members_count(self):
        return self.members.count()

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="projects")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")


class BlockManager(models.Manager):
    def todo_tasks(self):
        return self.filter(type=STATUS_CHOICES[1])

    def in_progress_tasks(self):
        return self.filter(type=STATUS_CHOICES[2])

    def done_tasks(self):
        return self.filter(type=STATUS_CHOICES[3])

    def new_tasks(self):
        return self.filter(type=STATUS_CHOICES[4])

    def filter_by_status(self, status):
        return self.filter(type=status)


class Block(models.Model):
    name = models.CharField(max_length=300)
    type = models.IntegerField(choices=STATUS_CHOICES, default=4)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="blocks")

    status_sort = BlockManager

    @property
    def tasks_count(self):
        return self.tasks.count()

    def __str__(self):
        return self.name + " " + str(self.project)


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="created_tasks")
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="assigned_tasks")
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="tasks")
    order = models.IntegerField()

    @property
    def documents_count(self):
        return self.documents.count()

    def __str__(self):
        return self.name + " With priority of " + str(self.order)


class TaskDocument(models.Model):
    document = models.FileField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="documents")

    def __str__(self):
        return self.document.name + " added by " + str(self.creator.full_name)


class TaskComment(models.Model):
    body = models.TextField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.creator.full_name + " posted at  " + str(self.created_at)
