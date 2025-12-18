from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like
from communities.models import Community


class PostAuthorSerializer(serializers.ModelSerializer):
    """Minimal user serializer for post author."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post - list and detail views."""
    author = PostAuthorSerializer(read_only=True)
    community_name = serializers.CharField(source='community.name', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'content', 'created_at', 
            'author', 'community', 'community_name',
            'like_count', 'is_liked'
        )
        read_only_fields = ('id', 'created_at', 'author')
    
    def get_is_liked(self, obj):
        """Check if current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new post."""
    class Meta:
        model = Post
        fields = ('id', 'content', 'community')
        read_only_fields = ('id',)
    
    def validate_community(self, value):
        """Validate that user is a member of the community."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from communities.models import CommunityMember
            is_member = CommunityMember.objects.filter(
                user=request.user,
                community=value
            ).exists()
            if not is_member:
                raise serializers.ValidationError(
                    "You must be a member of the community to post."
                )
        return value


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like."""
    user = serializers.StringRelatedField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'username', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
