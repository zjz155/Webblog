from django.contrib import admin

from blog.models import *
# Register your models here.
# admin.site.register(Blog)
admin.site.register(Comment)
# admin.site.register(Entry)
admin.site.register(Category)
admin.site.register(Reply)
admin.site.register(Test_Entry)

# @admin.register(Entry)
# class EntryAdmin(admin.ModelAdmin):
#     list_display = ("user", "headline", "abstract", "pub_date", "status")
#     def get_absolute_url(self):
#         pass

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class BlogAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)

class EntryAdmin(admin.ModelAdmin):
    inlines = (CategoryInline, CommentInline,)
    list_display = ("user", "headline", "abstract", "pub_date", "status")

    def get_absolute_url(self):
        pass


admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)