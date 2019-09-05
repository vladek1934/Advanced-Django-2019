from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


def file_category_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'category_{0}/{1}'.format(instance.category.id, filename)


class Label(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class PolygonManager(models.Manager):
    def for_user(self, user):
        return self.filter(created_by=user)


class CommentManager(models.Manager):
    def for_user(self, user):
        return self.filter(created_by=user)


class Folder(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=3000)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=3000)
    allowed = models.ManyToManyField(User)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, default=1, related_name='categories')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class Image(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')
    file = models.FileField(blank=False, null=False, upload_to=file_category_path)

    def __str__(self):
        return self.file.name


class Polygon(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, default=1)
    attributes = models.CharField(max_length=3000)
    points = models.CharField(max_length=5000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name='polygons')
    objects = PolygonManager()

    class Meta:
        verbose_name = 'Polygon'
        verbose_name_plural = 'Polygons'

    def __str__(self):
        return '{}: {}'.format(self.id, self.label.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.label.name
        }


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=3000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name='comments')
    objects = CommentManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return '{}: {}'.format(self.id, self.text)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.text
        }
