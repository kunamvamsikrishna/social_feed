from django.contrib import admin
from .models import Community, CommunityMember


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'member_count_display', 'post_count_display')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def member_count_display(self, obj):
        return obj.get_member_count()
    member_count_display.short_description = 'Members'
    
    def post_count_display(self, obj):
        return obj.get_post_count()
    post_count_display.short_description = 'Posts'


@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'community', 'joined_at')
    list_filter = ('joined_at', 'community')
    search_fields = ('user__username', 'community__name')
    readonly_fields = ('joined_at',)
    ordering = ('-joined_at',)
