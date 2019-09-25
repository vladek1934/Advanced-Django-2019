from django.contrib import admin
from base.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'creator')


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project',)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'project')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'order')


@admin.register(TaskDocument)
class TaskDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'creator', 'task')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'created_at', 'task')
