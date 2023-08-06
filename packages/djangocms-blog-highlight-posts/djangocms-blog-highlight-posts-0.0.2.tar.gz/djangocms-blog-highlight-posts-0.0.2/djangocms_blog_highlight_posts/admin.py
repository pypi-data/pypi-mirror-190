# Django
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third party
import djangocms_blog.admin as blog_admin

# Local application / specific library imports
from .models import PostHighlightExtension


class PostHighlightExtensionInline(admin.StackedInline):
    model = PostHighlightExtension
    fields = ["highlighted"]
    min_num = 1
    max_num = 1
    extra = 1
    can_delete = False
    verbose_name = _("Highlighting")


blog_admin.register_extension(PostHighlightExtensionInline)
