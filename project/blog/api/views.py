from rest_framework import permissions
from rest_framework import viewsets

from .serializers import PostSerializer
from blog.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().filter(
        is_published_to_telegram=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
