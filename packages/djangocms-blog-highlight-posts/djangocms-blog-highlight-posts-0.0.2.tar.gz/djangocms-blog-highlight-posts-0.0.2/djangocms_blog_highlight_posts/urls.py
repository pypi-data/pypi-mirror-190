# Django
from django.urls import path

# Third party
from djangocms_blog.urls import app_name  # noqa
from djangocms_blog.urls import urlpatterns as blog_urls

# Local application / specific library imports
from .views import PostHighlightListView

urlpatterns = [
    path("", PostHighlightListView.as_view(), name="posts-latest"),
] + blog_urls
