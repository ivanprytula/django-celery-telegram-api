from rest_framework import permissions
from rest_framework import viewsets

from .serializers import CustomUserSerializer
from .serializers import PostSerializer
from accounts.models import CustomUser
from blog.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().filter(
        is_published_to_telegram=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CustomUsers to be viewed or edited.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = CustomUser.objects.filter(id=self.request.user.id)
        if self.request.user.is_superuser:
            queryset = CustomUser.objects.all()
        return queryset
