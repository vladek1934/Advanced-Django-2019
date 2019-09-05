from django.contrib import admin
from main.models import Image, Polygon, Category, Comment, Label, Folder


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'category_name', 'category_id')

    def category_name(self, obj):
        return obj.category.name

    def category_id(self, obj):
        return obj.category.id

    category_name.admin_order_field = 'Category name'  # Allows column order sorting
    category_name.short_description = 'Category Name'  # Renames column head

    category_id.admin_order_field = 'Category id'  # Allows column order sorting
    category_id.short_description = 'Category id'  # Renames column head


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'label', 'image', 'created_by', 'attributes')


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'folder')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'created_by', 'text', 'image')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
