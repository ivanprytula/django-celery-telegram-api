from django.urls import path, include
from rest_framework import routers

from .api import views as api_views
from .views import (
    BlogListView,
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
    path('', BlogListView.as_view(), name='blog_list'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<category>/', BlogCategory.as_view(), name='post_category'),
]
