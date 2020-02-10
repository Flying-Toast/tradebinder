from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Binder, Have, Want


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Binder)
admin.site.register(Have)
admin.site.register(Want)
