from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reply_to', 'content_object', 'root', 'parent', 'text', 'comment_time')
