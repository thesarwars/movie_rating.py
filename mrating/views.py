from django.shortcuts import render, get_object_or_404
from .models import User, MovieRating, Movie
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'msg': 'User Login Successfull'})
        else:
            return JsonResponse({'msg': 'Invalid email or passowrd'}, status = 401)
    else:
        return JsonResponse({"msg": "Method is not Allowed"}, status=405)
    
 
@csrf_exempt    
def add_movie(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        genre = request.POST.get('genre')
        rating = request.POST.get('rating')
        release_date = request.POST.get('release_date')
        
        movie = Movie.objects.create(name=name, genre=genre, rating=rating, release_date=release_date)
        return JsonResponse({'msg': f'Movie "{name}" addes successfully'}, status=201)
    else:
        return JsonResponse({'msg': "Movie not added in the database"}, status=400)
    
    
@csrf_exempt
def get_movies(request):
    movie_list = Movie.objects.all()
    return JsonResponse({'msg': [movie.name for movie in movie_list]})


@csrf_exempt
def rate_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, pk=movie_id)
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        rating = request.POST.get('rating')
        
        MovieRating.objects.create(movie_id=movie, user_id=user, rating=rating)
        return JsonResponse({'msg': f'{user.name} rated {movie.name} {rating} out of 5'}, status=201)
    else:
        return JsonResponse({"msg": "Method is not Allowed"}, status=405)
        
        

# @csrf_exempt
# def search_movie(request):
#     name = request.GET.get('name')
#     try:
#         movie = Movie.objects.get(name=name)
#         ratings = MovieRating.objects.filter(movie_id=movie)
#         avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
#         return JsonResponse({'name': movie.name, 'avg_rating': avg_rating})  # Use movie.name for clarity
#     except Movie.DoesNotExist as e:
#         return JsonResponse({'message': str(e)}, status=404)


@csrf_exempt
def search_movie(request):
    name = request.GET.get('name')
    movies = Movie.objects.filter(name=name).exists()
    print(movies)
    if movies:
        movie = Movie.objects.get(name=name)
        ratings = MovieRating.objects.filter(movie_id=movie)
        avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
        return JsonResponse({'name': movie.name, 'avg_rating': avg_rating})
    else:
        return JsonResponse({'message': 'Movie not found'}, status=404)
