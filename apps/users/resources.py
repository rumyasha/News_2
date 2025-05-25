from import_export import resources, fields
from .models import User


class UserResource(resources.ModelResource):
    full_name = fields.Field(column_name='full_name', attribute='get_full_name')

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'is_active', 'date_joined')
        export_order = fields