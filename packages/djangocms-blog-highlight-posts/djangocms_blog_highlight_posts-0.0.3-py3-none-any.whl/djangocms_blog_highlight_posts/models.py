# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third party
from djangocms_blog.models import Post


class PostHighlightExtension(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="highlight_extension"
    )

    highlighted = models.BooleanField(
        verbose_name=_("Highlight post"),
        default=False,
        db_index=True,
        help_text=_("Highlight this post in the blog list"),
    )

    class Meta:
        verbose_name = _("Post highlight extension")
        verbose_name_plural = _("Post highlight extensions")
