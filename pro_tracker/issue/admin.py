from django.contrib import admin
from .models import Issue, Comment
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Issue, MarkdownxModelAdmin)
admin.site.register(Comment, MarkdownxModelAdmin)

