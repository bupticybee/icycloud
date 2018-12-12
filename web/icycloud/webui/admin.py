from django.contrib import admin

# Register your models here.

from .models import InviteCode

class InviteCodeAdmin(admin.ModelAdmin):
    list_display=('code','used')

admin.site.register(InviteCode,InviteCodeAdmin)
