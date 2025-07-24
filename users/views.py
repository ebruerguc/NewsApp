from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login  
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordChangeView

class SignUpView(CreateView):

    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_invalid(self, form):
        
        print("Form Hataları:")
        for field, errors in form.errors.items():
            print(f"  Alan '{field}': {', '.join(errors)}")
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response

class CustomPasswordChangeView(PasswordChangeView):
    template_name= 'registration/password_change.html'
    success_url= reverse_lazy('password_change_done')


def article_create(request):
    return render(request, 'articles/article_form.html')
