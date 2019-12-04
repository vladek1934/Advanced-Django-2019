import logging

from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from base.utils.ChoiceFields import *
from base.models import Task, MainUser, Profile, Project, Block, TaskDocument
from base.utils.document_upload import task_delete_path

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Project.objects.create(name='Default example',
                               description='Starter tutorial project. You can delete it anytime, if you want!',
                               creator=instance)
        user_logger.info(f"{instance} registered!\n")
        print(instance)


@receiver(post_save, sender=TaskDocument)
def document_created(sender, instance, created, **kwargs):
    if created:
        actions_logger.info(f"{instance.document} created by {instance.creator} !\n")
        print(instance)


@receiver(post_save, sender=Project)
def project_created(sender, instance, created, **kwargs):
    if created:
        actions_logger.info(f"{instance.creator} created project {instance.id, instance.name}!\n")
        Block.objects.create(name='To do', type=STATUS_TODO, project=instance)
        Block.objects.create(name='In process', type=STATUS_IN_PROGRESS, project=instance)
        Block.objects.create(name='Done', type=STATUS_DONE, project=instance)
        print(instance)


@receiver(post_delete, sender=TaskDocument)
def document_deleted(sender, instance, **kwargs):
    print('started deleting doc')
    if instance:
        task_delete_path(document=instance)
        print('deleted')
