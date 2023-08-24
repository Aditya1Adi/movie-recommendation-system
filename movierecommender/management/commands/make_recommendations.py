from django.core.management import BaseCommand
from ...models import Movie


# Check if genres are valid
def check_valid_genres(genres: str) -> bool:
    if bool(genres and not genres.isspace()) and genres != 'na':
        return True
    else:
        return False


# Add a Jaccard similarity method here
def jaccand_similarity(list1: list, list2: list) -> float:
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))


# Add a movie similarity method here
def similarity_between_movies(movie1: Movie, movie2: Movie) -> float:
    if check_valid_genres(movie1.genres) and check_valid_genres(movie2.genres):
        m1_generes = movie1.genres.split()
        m2_generes = movie2.genres.split()
        return jaccand_similarity(m1_generes, m2_generes)

    else:
        return 0


class Command(BaseCommand):
    help = 'Recommend movies'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        # Figure the recommended field for each unwatched movie
        # Based on the similarity on movie genres
        pass


# python manage.py make_recommendations
# Calculate the similarity between two movies

def similarity_between_movies(movie1: Movie, movie2: Movie) -> float:
    if check_valid_genres(movie1.genres) and check_valid_genres(movie2.genres):
        m1_genres = movie1.genres.split()
        m2_genres = movie2.genres.split()
        return jaccand_similarity(m1_genres, m2_genres)

    else:
        return 0


def handle(self, *args, **kwargs):
    THRESHOLD = 0.8

    # Get all watched and unwatched movies
    watched_movies = Movie.objects.filter(watched=True)
    unwatched_movies = Movie.objects.filter(watched=False)

    # Start to generate recommendations in unwatched movies
    for unwatched_movie in unwatched_movies:
        max_similarity = 0

        # for each watched movie
        for watched_movie in watched_movies:
            # Calculate the similarity between each watched movie and its recommendations all unwatched movies
            similarity = similarity_between_movies(unwatched_movie, watched_movie)
            if similarity >= max_similarity:
                max_similarity = similarity

            # early stop if the unwatched_movie is similar enough
            if max_similarity >= THRESHOLD:
                break

        # if the unwatched_movie is not similar enough to any watched_movie, then recommend it
        if max_similarity > THRESHOLD:
            print(f"Find a movie recommendation: {unwatched_movie.original_title}")
            # Update the recommendation status for the current movie (e.g., unwatched_movie.recommended = True)
            # unwatched_movie.save() # Uncomment and implement the update in your Movie model



