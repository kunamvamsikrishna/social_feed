from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count
from .models import Community, CommunityMember
from .serializers import (
    CommunitySerializer, 
    CommunityCreateSerializer, 
    CommunityDetailSerializer,
    CommunityMemberSerializer
)


class CommunityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Community CRUD operations.
    
    list: GET /api/communities/ - List all communities
    retrieve: GET /api/communities/{id}/ - Get community details
    create: POST /api/communities/ - Create new community
    update: PUT /api/communities/{id}/ - Update community (creator only)
    partial_update: PATCH /api/communities/{id}/ - Partial update (creator only)
    destroy: DELETE /api/communities/{id}/ - Delete community (creator only)
    join: POST /api/communities/{id}/join/ - Join community
    leave: POST /api/communities/{id}/leave/ - Leave community
    members: GET /api/communities/{id}/members/ - Get community members
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Annotate queryset with counts."""
        return Community.objects.annotate(
            member_count=Count('members', distinct=True),
            post_count=Count('posts', distinct=True)
        ).select_related('created_by').order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return CommunityCreateSerializer
        elif self.action == 'retrieve':
            return CommunityDetailSerializer
        return CommunitySerializer
    
    def perform_create(self, serializer):
        """Set the creator as the current user."""
        serializer.save(created_by=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """Only creator can update community."""
        community = self.get_object()
        if community.created_by != request.user:
            return Response(
                {'error': 'Only the creator can update this community'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only creator can delete community."""
        community = self.get_object()
        if community.created_by != request.user:
            return Response(
                {'error': 'Only the creator can delete this community'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        """
        POST /api/communities/{id}/join/
        Join a community.
        """
        community = self.get_object()
        user = request.user
        
        # Check if already a member
        if CommunityMember.objects.filter(user=user, community=community).exists():
            return Response(
                {'message': 'You are already a member of this community'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership
        CommunityMember.objects.create(user=user, community=community)
        
        return Response(
            {'message': f'Successfully joined {community.name}'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, pk=None):
        """
        POST /api/communities/{id}/leave/
        Leave a community.
        """
        community = self.get_object()
        user = request.user
        
        # Check if creator
        if community.created_by == user:
            return Response(
                {'error': 'Community creator cannot leave their own community'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if member
        membership = CommunityMember.objects.filter(user=user, community=community).first()
        if not membership:
            return Response(
                {'error': 'You are not a member of this community'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete membership
        membership.delete()
        
        return Response(
            {'message': f'Successfully left {community.name}'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """
        GET /api/communities/{id}/members/
        Get list of community members.
        """
        community = self.get_object()
        members = community.members.select_related('user').order_by('-joined_at')
        serializer = CommunityMemberSerializer(members, many=True)
        return Response(serializer.data)

