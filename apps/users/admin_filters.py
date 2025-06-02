from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class ActiveUserFilter(admin.SimpleListFilter):
    """Фильтр по активности пользователя"""
    title = _('Активность')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('active', _('Активные')),
            ('inactive', _('Неактивные')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

class StaffFilter(admin.SimpleListFilter):
    """Фильтр по статусу персонала"""
    title = _('Персонал')
    parameter_name = 'staff'

    def lookups(self, request, model_admin):
        return (
            ('staff', _('Персонал')),
            ('non_staff', _('Обычные пользователи')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'staff':
            return queryset.filter(is_staff=True)
        if self.value() == 'non_staff':
            return queryset.filter(is_staff=False)