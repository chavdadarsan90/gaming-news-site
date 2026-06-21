from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Import this guard
from news.models import Article # Import Article to pull bookmarks

@login_required
def profile(request):
    # Fetch all articles where this specific user exists in the bookmarks field
    saved_articles = Article.objects.filter(bookmarks=request.user).order_by('-published_at')
    
    return render(request, 'users/profile.html', {'saved_articles': saved_articles})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # FIX: Changed form.is_form_valid() to form.is_valid()
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})