from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Movies, Rating, WatchList, BucketList
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def home(request):
    movies=Movies.objects.all()[:10]
    return render(request,'base.html',{'movies':movies})
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                # Redirect to admin dashboard or any other admin-specific page
                return redirect('/admin/')
            else:
                # Redirect to user dashboard or any other user-specific page
                return redirect('dashboard')


    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def movie_search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        movies = Movies.objects.filter(original_title__icontains=query)[:10]
        return render(request, 'movie_search.html', {'movies': movies})

    return render(request, 'movie_search.html')

@login_required
def movie_detail(request, imdb_id):
    if not request.user.is_authenticated:
        return redirect("login")

    movies = get_object_or_404(Movies,imdb_id=imdb_id)
    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Rating()
        ratingObject.user = request.user
        ratingObject.movie = movies
        ratingObject.rating = rate
        ratingObject.save()
        messages.success(request, "Your Rating is submited ")
        return redirect('movie_detail',imdb_id=imdb_id)
    return render(request, 'movie_detail.html', {'movies': movies})

@login_required
def user_profile(request):
    user_profile = request.user
    return render(request, 'user_profile.html', {'user_profile': user_profile})
def movie_recommendations(request, imdb_id):
    # Get the selected movie from the database
    selected_movie = get_object_or_404(Movies, imdb_id=imdb_id)

    # Fetch all movies from the database (excluding the selected movie)
    all_movies = Movies.objects.exclude(imdb_id=imdb_id)

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform([movie.overview for movie in all_movies])

    # Compute the cosine similarity between the selected movie and all other movies
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_vectorizer.transform([selected_movie.overview]))
    similarity_scores = list(enumerate(cosine_sim.flatten()))

    # Sort movies based on similarity scores
    similar_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Retrieve the top 5 recommended movies from the sorted list and include the poster_path attribute
    recommended_movies = [
        {
            "original_title": all_movies[i].original_title,
            "overview": all_movies[i].overview,
            "poster_path": all_movies[i].poster_path,
        }
        for i, _ in similar_movies[:5]
    ]

    # Return the recommended movies in the template
    context = {
        'selected_movie': selected_movie,
        'recommended_movies': recommended_movies,
    }
    return render(request, 'movie_recommendations.html', context)


@login_required()
def add_to_bucket_list(request, imdb_id):
    if request.user.is_authenticated:
        movie = Movies.objects.get(imdb_id=imdb_id)
        if BucketList.objects.filter(movie=movie, user=request.user).exists():
            messages.warning(request, "Movie is already in your bucket list.",fail_silently=True)
        else:
            BucketList.objects.create(user=request.user, movie=movie)
            messages.success(request, "Movie added to your bucket list.",fail_silently=True)
        return redirect('bucket_list')
    else:
        return redirect('login')

@login_required()
def bucket_list(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            imdb_id = request.POST.get('imdb_id')
            BucketList.objects.filter(movie__imdb_id='imdb_id', user=request.user).delete()

        bucket_list = BucketList.objects.filter(user=request.user)
        return render(request, 'bucket_list.html', {'bucket_list': bucket_list})
    else:
        return redirect('login')

@login_required()
def remove_from_bucket_list(request, imdb_id):
    if request.user.is_authenticated:
        bucket_list_item = BucketList.objects.filter(movie__imdb_id=imdb_id, user=request.user)
        bucket_list_item.delete()
    return redirect('bucket_list')

@login_required()
def watch_list(request):
    if not request.user.is_authenticated:
        return redirect("login")

    watch_list_items = WatchList.objects.filter(user=request.user)

    return render(request, 'watch_list.html', {'watch_list_items': watch_list_items})

@login_required()
def add_to_watch_list(request,imdb_id):
    if request.user.is_authenticated:
        movie = Movies.objects.get(imdb_id=imdb_id)
        if WatchList.objects.filter(movie=movie, user=request.user).exists():
            messages.warning(request, "Movie is already in your watched list.",fail_silently=True)
        else:
            BucketList.objects.create(user=request.user, movie=movie)
            messages.success(request, "Movie added to your watched list.",fail_silently=True)
        return redirect('watch_list')
    else:
        return redirect('login')


