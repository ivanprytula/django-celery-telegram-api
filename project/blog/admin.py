from django.contrib import admin

from blog.models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    """Post model for Django administration."""
    list_display = ('title', 'slug', 'author', 'created_at')
    list_filter = ('is_published_to_telegram',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    """Comment model for Django administration."""
    list_display = ('commenter_name', 'content', 'post', 'created_at',
                    'active')
    list_filter = ('active', 'created_at')
    search_fields = ('commenter_name', 'author', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class CategoryAdmin(admin.ModelAdmin):
    """Category model for Django administration."""


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
