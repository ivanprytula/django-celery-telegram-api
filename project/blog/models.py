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


class Comment(models.Model):
    """Comment to post from other user."""
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    content = models.TextField(blank=False, default='Enter your comment...')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author)


class Category(models.Model):
    """Categories to which post can belong."""
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
