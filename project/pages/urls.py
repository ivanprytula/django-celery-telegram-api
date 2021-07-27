from django.urls import path, include

from .sandbox_views import (
    see_request,
    user_info,
    private_place,
    staff_place,
    add_messages,
)
from .views import AboutPageView, HomePageView

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
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('test/', include(extra_patterns)),

]
