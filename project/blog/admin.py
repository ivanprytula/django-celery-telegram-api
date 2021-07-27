from django.contrib import admin

from blog.models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    """Post model for Django administration."""


class CommentAdmin(admin.ModelAdmin):
    """Comment model for Django administration."""


class CategoryAdmin(admin.ModelAdmin):
    """Category model for Django administration."""


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
