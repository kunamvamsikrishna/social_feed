from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Community, CommunityMember


class CommunityMemberSerializer(serializers.ModelSerializer):
    """Serializer for CommunityMember."""
    user = serializers.StringRelatedField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CommunityMember
        fields = ('id', 'user', 'username', 'joined_at')
        read_only_fields = ('id', 'joined_at')


class CommunitySerializer(serializers.ModelSerializer):
    """Serializer for Community - list and detail views."""
    created_by = serializers.StringRelatedField()
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Community
        fields = (
            'id', 'name', 'description', 'created_at', 
            'created_by', 'created_by_id', 'member_count', 
            'post_count', 'is_member'
        )
        read_only_fields = ('id', 'created_at', 'created_by')
    
    def get_is_member(self, obj):
        """Check if current user is a member."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommunityMember.objects.filter(
                user=request.user,
                community=obj
            ).exists()
        return False


class CommunityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new community."""
    class Meta:
        model = Community
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class CommunityDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Community - includes members list."""
    created_by = serializers.StringRelatedField()
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    members = CommunityMemberSerializer(many=True, read_only=True)
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Community
        fields = (
            'id', 'name', 'description', 'created_at', 
            'created_by', 'created_by_id', 'member_count', 
            'post_count', 'members', 'is_member'
        )
        read_only_fields = ('id', 'created_at', 'created_by')
    
    def get_is_member(self, obj):
        """Check if current user is a member."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommunityMember.objects.filter(
                user=request.user,
                community=obj
            ).exists()
        return False
