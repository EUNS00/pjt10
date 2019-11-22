from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from movies.models  import Movie
from .forms import CustumUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from IPython import embed

def index(request):
    users = User.objects.all()
    context = {'users': users,}
    return render(request, 'accounts/index.html', context)

def detail(request,user_pk):
    user = User.objects.get(pk=user_pk)
    like_movies = user.like_movies.filter(pk=user_pk)
    person = get_object_or_404(get_user_model(), pk=user_pk)
    context = {'user':user, 'like_movies':like_movies, 'person': person}
    embed()
    return render(request, 'accounts/detail.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustumUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustumUserCreationForm()
    context = {'form': form, }
    return render(request, 'accounts/auth_form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {'form': form, }
    return render(request, 'accounts/auth_form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')
    

@login_required
def follow(request, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    embed()
    if person.followers.filter(pk=user.pk).exists():
        person.followers.remove(user)
    else:
        person.followers.add(user)
    return redirect('accounts:detail', user_pk)