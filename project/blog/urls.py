from django.urls import include
from django.urls import path
from rest_framework import routers

from .api import views as api_views
from .views import BlogCategory
from .views import PostCreateView
from .views import PostDeleteView
from .views import PostDetailView
from .views import PostListView
from .views import PostUpdateView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(r'posts', api_views.PostViewSet, 'post')
router.register(r'users', api_views.CustomUserViewSet, basename='customuser')


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('blog/create/', PostCreateView.as_view(), name='post-create'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('blog/update/<int:pk>/', PostUpdateView.as_view(),
         name='post-update'),
    path('blog/delete/<int:pk>/', PostDeleteView.as_view(),
         name='post-delete'),
    path('tags/<category>/', BlogCategory.as_view(), name='post-category'),
]
