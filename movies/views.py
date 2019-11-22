from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Genre, Movie, Review
from .forms import ReviewForm
from IPython import embed

def index(request):
    movies = Movie.objects.all()
    context = { 'movies' : movies, }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    review_form = ReviewForm()
    context = { 'movie' : movie ,'review_form': review_form, 'reviews': reviews,}
    return render(request, 'movies/detail.html', context)

@login_required
def review_create(request, movie_pk):
    review_form = ReviewForm(request.POST)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.movie_id = movie_pk
        review.user = request.user
        review.save()
    return redirect('movies:detail',movie_pk)

@login_required
def review_delete(request, movie_pk, review_pk):
    
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('movies:detail', movie_pk)

@login_required
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)  
    else:
        movie.like_users.add(user)
    return redirect('movies:detail', movie_pk)

