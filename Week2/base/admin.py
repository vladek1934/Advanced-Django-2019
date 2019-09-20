from django.contrib import admin
from base.models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user',)
