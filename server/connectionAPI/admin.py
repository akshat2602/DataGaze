from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .models import *

# Register your models here.
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields',
            {
                'fields': (
                    'mtm_database',
                    'name'
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)



admin.site.register(Database)
admin.site.register(Field)
admin.site.register(Table)