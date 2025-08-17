from django.contrib import admin
from .models import *
# Register your models here.

class Inline(admin.TabularInline):
    model = Attribut
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title"]
    inlines =  [Inline]
    exclude = ['final_price']


admin.site.register(Article,ArticleAdmin)
