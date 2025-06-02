from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser  # Изменяем User на CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser  # Используем CustomUser
        fields = ('email',)  # Только email при регистрации

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser  # Используем CustomUser
        fields = '__all__'