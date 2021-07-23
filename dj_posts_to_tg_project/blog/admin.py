from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    """Post model for Django administration."""


admin.site.register(Post, PostAdmin)
