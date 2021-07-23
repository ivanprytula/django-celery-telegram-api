from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    """Represents post in blog app."""
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name='user_posts')
    title = models.CharField(max_length=255, blank=False,
                             default='Enter title...')
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_published_to_telegram = models.BooleanField(default=False)

    class Meta:
        """Indicated field used for ordering."""
        ordering = ['-created_at']

    def __str__(self):
        return self.title
