from django.urls import path, include
from rest_framework import routers

from .api import views as api_views
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    BlogCategory,
)

router = routers.DefaultRouter()
router.register(r'posts', api_views.PostViewSet)

app_name = 'blog'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    # path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('blog/create/', PostCreateView.as_view(), name='post-create'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('tags/<category>/', BlogCategory.as_view(), name='post-category'),
]
