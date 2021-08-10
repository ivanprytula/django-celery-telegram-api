from django.urls import include
from django.urls import path

from .sandbox_views import add_messages
from .sandbox_views import private_place
from .sandbox_views import see_request
from .sandbox_views import staff_place
from .sandbox_views import user_info
from .views import AboutPageView
from .views import LinksDepotView
from .views import MindMapView

app_name = 'pages'

# testing urls
extra_patterns = [
    path('see_request/', see_request),
    path('user_info/', user_info),
    path('private_place/', private_place),
    path('staff_place/', staff_place),
    path('add_messages/', add_messages),
]

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('links-depot/', LinksDepotView.as_view(), name='links-depot'),
    path('python-mind-map/', MindMapView.as_view(), name='python-mind-map'),
    path('test/', include(extra_patterns)),

]
