from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AccountUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AccountUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = AccountUser
        fields = ('email',)
