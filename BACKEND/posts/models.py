from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from communities.models import Community, CommunityMember


class Post(models.Model):
    """
    Represents content created by users inside communities.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['community', '-created_at']),
        ]

    def __str__(self):
        return f"{self.author.username} - {self.community.name} ({self.created_at.strftime('%Y-%m-%d')})"

    def get_like_count(self):
        """Return the number of likes on this post."""
        return self.likes.count()

    def is_liked_by(self, user):
        """Check if a specific user has liked this post."""
        return self.likes.filter(user=user).exists()

    def clean(self):
        """
        Validate that the author is a member of the community.
        """
        super().clean()
        if self.author and self.community:
            is_member = CommunityMember.objects.filter(
                user=self.author,
                community=self.community
            ).exists()
            
            if not is_member:
                raise ValidationError(
                    f"User {self.author.username} must be a member of {self.community.name} to create a post."
                )

    def save(self, *args, **kwargs):
        """
        Override save to call clean() for validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)


class Like(models.Model):
    """
    Represents a user liking a post.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can like a post only once
        unique_together = ('user', 'post')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"
