from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer, PostCreateSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post CRUD operations.
    
    list: GET /api/posts/ - List all posts (optionally filter by community)
    retrieve: GET /api/posts/{id}/ - Get post details
    create: POST /api/posts/ - Create new post (must be community member)
    update: PUT /api/posts/{id}/ - Update post (author only)
    partial_update: PATCH /api/posts/{id}/ - Partial update (author only)
    destroy: DELETE /api/posts/{id}/ - Delete post (author only)
    like: POST /api/posts/{id}/like/ - Toggle like on post
    likes: GET /api/posts/{id}/likes/ - Get list of users who liked post
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Get posts with annotations for like count."""
        user = self.request.user
        queryset = Post.objects.select_related(
            'author', 'community'
        ).annotate(
            like_count=Count('likes', distinct=True)
        ).order_by('-created_at')
        
        # Filter by community if provided
        community_id = self.request.query_params.get('community')
        if community_id:
            queryset = queryset.filter(community_id=community_id)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Set the author as the current user."""
        serializer.save(author=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create post and return full serialized data."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return full post data with PostSerializer
        post = serializer.instance
        output_serializer = PostSerializer(post, context={'request': request})
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Only author can update post."""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'Only the author can update this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only author can delete post."""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'Only the author can delete this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        POST /api/posts/{id}/like/
        Toggle like on a post (like if not liked, unlike if already liked).
        Only community members can like posts.
        """
        post = self.get_object()
        user = request.user
        
        # Check if user is a member of the community
        from communities.models import CommunityMember
        is_member = CommunityMember.objects.filter(
            user=user,
            community=post.community
        ).exists()
        
        if not is_member:
            return Response(
                {'error': 'You must be a member of the community to like posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already liked
        like = Like.objects.filter(user=user, post=post).first()
        
        if like:
            # Unlike
            like.delete()
            return Response(
                {
                    'message': 'Post unliked',
                    'is_liked': False,
                    'like_count': post.likes.count()
                },
                status=status.HTTP_200_OK
            )
        else:
            # Like
            Like.objects.create(user=user, post=post)
            return Response(
                {
                    'message': 'Post liked',
                    'is_liked': True,
                    'like_count': post.likes.count()
                },
                status=status.HTTP_201_CREATED
            )
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """
        GET /api/posts/{id}/likes/
        Get list of users who liked this post.
        """
        post = self.get_object()
        likes = post.likes.select_related('user').order_by('-created_at')
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class CommunityPostListView(generics.ListAPIView):
    """
    GET /api/communities/{community_id}/posts/
    Get all posts for a specific community (feed view).
    Only accessible to community members.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get posts for specific community if user is a member."""
        community_id = self.kwargs['community_id']
        user = self.request.user
        
        # Check if user is a member
        from communities.models import CommunityMember
        is_member = CommunityMember.objects.filter(
            user=user,
            community_id=community_id
        ).exists()
        
        if not is_member:
            return Post.objects.none()
        
        return Post.objects.filter(
            community_id=community_id
        ).select_related(
            'author', 'community'
        ).annotate(
            like_count=Count('likes', distinct=True)
        ).order_by('-created_at')

