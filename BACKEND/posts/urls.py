from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommunityPostListView

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('community/<int:community_id>/', CommunityPostListView.as_view(), name='community-posts'),
]
