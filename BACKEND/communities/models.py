from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    """
    Represents a community created by a user.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_communities'
    )

    class Meta:
        verbose_name_plural = 'Communities'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_member_count(self):
        """Return the number of members in this community."""
        return self.members.count()

    def get_post_count(self):
        """Return the number of posts in this community."""
        return self.posts.count()

    def save(self, *args, **kwargs):
        """
        Override save to automatically add creator as a member.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Automatically add creator as a member
            CommunityMember.objects.get_or_create(
                user=self.created_by,
                community=self
            )


class CommunityMember(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='community_memberships'
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='members'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can join a community only once
        unique_together = ('user', 'community')
        ordering = ['-joined_at']
        indexes = [
            models.Index(fields=['-joined_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.community.name}"
