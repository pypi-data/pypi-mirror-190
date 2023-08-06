# Django
from django.db.models.expressions import Case, When
from django.db.models.fields import BooleanField

# Third party
from djangocms_blog.models import Post
from djangocms_blog.views import PostListView

HIGHLIGHT_QUERYSET_ORDERING = (
    "-highlighted",
    *Post._meta.ordering,
)


class PostHighlightListView(PostListView):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                highlighted=Case(
                    When(highlight_extension__highlighted=True, then=True),
                    default=False,
                    output_field=BooleanField(),
                )
            )
            .order_by(*HIGHLIGHT_QUERYSET_ORDERING)
        )
