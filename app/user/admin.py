from django.contrib import admin

from .models import User

# Register your models here.
class AdminUser(admin.ModelAdmin):
    class Meta:
        model = User

admin.site.register(User, AdminUser)