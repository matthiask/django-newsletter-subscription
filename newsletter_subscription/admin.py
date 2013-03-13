from django.contrib import admin

from . import models


admin.site.register(models.Subscription,
    list_display=('email', 'is_active', 'full_name'),
    list_filter=('is_active',),
    search_fields=('email', 'full_name'),
    )
