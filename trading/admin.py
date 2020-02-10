from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Binder, Have, Want


class HaveInline(admin.TabularInline):
    model = Have
    readonly_fields = ("card",)

class WantInline(admin.TabularInline):
    model = Want
    readonly_fields = ("oracle_id", "set")

class BinderAdmin(admin.ModelAdmin):
    inlines = [HaveInline, WantInline]

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Binder, BinderAdmin)
