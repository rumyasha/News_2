from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class ActiveUserFilter(admin.SimpleListFilter):
    title = _('Active status')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('active', _('Active')),
            ('inactive', _('Inactive')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)