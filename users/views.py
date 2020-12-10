from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics

from . import serializers
from .forms import CustomUserCreationForm
from .models import AccountUser


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserListView(generics.ListAPIView):
    queryset = AccountUser.objects.all()
    serializer_class = serializers.UserSerializer
