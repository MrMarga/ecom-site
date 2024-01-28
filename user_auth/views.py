from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.shortcuts import render, redirect 
from .forms import UserRegisterForm  # Make sure to replace '.forms' with the actual path to your forms module
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


User = settings.AUTH_USER_MODEL # importing Main user from settings.py of admin

def register_view(request):
    if request.method == 'POST':
        messages.warning(request,f'Hey, you login already.! ')
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}! Your account was created successfully.")
            
            # Use form.cleaned_data.get('email') and form.cleaned_data.get('password1') instead of square brackets
            new_user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            login(request, new_user)
            
            
            return redirect('index')  # 'index.html' should be just 'index' if it's the name of your URL pattern

    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request,'signup.html', context)




class CustomLoginView(LoginView):
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'You are already logged in.')
            return self.form_invalid(form)

        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully logged in.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Invalid username or password.')
        return response

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You are not logged in.')
            return self.http_method_not_allowed(request, *args, **kwargs)

        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'You have successfully logged out.')
        return response