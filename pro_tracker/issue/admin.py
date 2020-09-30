from django.contrib import admin
from .models import Issue
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Issue, MarkdownxModelAdmin)

