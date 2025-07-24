from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import CustomUserCreationForm

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


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    """
    Özelleştirilmiş parola değiştirme view'ı.
    Kullanıcıyı admin paneline değil, ana sayfaya yönlendirir.
    """
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Parolanız başarıyla değiştirildi.')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Admin kullanıcısı değilse ana sayfaya yönlendir
        if not self.request.user.is_staff:
            return reverse_lazy('home')
        # Admin kullanıcısı ise settings'deki ayarı kullan veya admin paneline git
        return super().get_success_url()


def article_create(request):
    return render(request, 'articles/article_form.html')
