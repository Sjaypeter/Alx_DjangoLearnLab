from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/templates/register.html'
#This usercreation orm handles user registration and when a user is registered they are redirected to the login page using the successurl




@login_required
def profile_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")  # Reloads the profile page
    else:
        form = AuthenticationForm()

    return render(request, "blog/templates/profile.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
            return render('blog/templates/login.html', {'form': form})
        
def logout_view(request):
    logout(request)
    return render(request, 'blog/templates/logout.html')
