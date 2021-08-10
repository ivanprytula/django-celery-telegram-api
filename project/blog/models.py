from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """Post model with MTM relation with Category."""
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name='user_posts')
    title = models.CharField(max_length=255, blank=False,
                             default='Enter title...')
    slug = models.SlugField(null=False, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(to='Category', related_name='posts')
    is_published_to_telegram = models.BooleanField(default=False)

    class Meta:
        """Indicated field used for ordering."""
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    @property
    def count_comments_under_moderation(self):
        return self.comments.filter(active=False).count()

    def comments_under_moderation(self):
        return self.comments.filter(active=False)


class Comment(models.Model):
    """Comment to post from other user."""
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE,
                             related_name='comments')
    commenter_name = models.CharField(max_length=80, default='NoName User')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment {self.content} by {self.commenter_name}'

    def get_model_name(self):
        return self.__class__.__name__


class Category(models.Model):
    """Categories to which post can belong."""
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
