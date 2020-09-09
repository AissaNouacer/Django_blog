from django.contrib import admin

from .models import Post, Comment, ImagePost


class ImagePostAdmin(admin.StackedInline):
    model = ImagePost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    prepopulated_field = {'slug':('title',)}
    raw_id_field = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [ImagePostAdmin]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    pass
