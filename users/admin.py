from django.contrib import admin

from users.models import User
from baskets.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'age', 'email', 'date_joined')
    ordering = ('username',)
    inlines = (BasketAdmin,)
