from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from base.utils.ChoiceFields import *
from base.models import Task, MainUser, Profile, Project, Block, TaskDocument
from base.utils.document_upload import task_delete_path


# @receiver(pre_delete, sender=Task)
# def task_deleted(sender, instance, **kwargs):
#     print('started deleting docs')
#     print(instance.documents)
#     print(instance.documents.count())
#     if instance.documents.count() > 0:
#         print('started deleting many docs')
#         for i in instance.documents:
#             task_delete_path(document=i)
#             print('deleted' + i)

@receiver(post_delete, sender=TaskDocument)
def document_deleted(sender, instance, **kwargs):
    print('started deleting doc')
    if instance:
        task_delete_path(document=instance)
        print('deleted')


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # instance.send_greeting_email()
        # instance.send_activate_sms()
    print(instance)


@receiver(post_save, sender=Project)
def project_created(sender, instance, created, **kwargs):
    if created:
        Block.objects.create(name='To do', type=STATUS_TODO, project=instance)
        Block.objects.create(name='In process', type=STATUS_IN_PROGRESS, project=instance)
        Block.objects.create(name='Done', type=STATUS_DONE, project=instance)
        print(instance.blocks)
