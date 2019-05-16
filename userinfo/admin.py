from django.contrib import admin

from userinfo.models import *
# admin.site.register(UserInfo)
admin.site.register(Contact)


# class ContactInline(admin.TabularInline):
#     model=Contact


class UserInfoAdmin(admin.ModelAdmin):
    # inlines = (ContactInline,)
    list_display = ("username", "is_active", "is_superuser")


admin.site.register(UserInfo, UserInfoAdmin)