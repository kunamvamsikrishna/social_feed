from django.contrib import admin
from .models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'community', 'content_preview', 'created_at', 'like_count_display')
    list_filter = ('created_at', 'community')
    search_fields = ('content', 'author__username', 'community__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def like_count_display(self, obj):
        return obj.get_like_count()
    like_count_display.short_description = 'Likes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
