# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# Part of the code is quoted from BUS216 Professor Namini's class notes

import random
import pandas as pd
from Tag import Tag
from Movie import Movie
from Rating import Rating

# the website is recommending randomly
random.seed(6)


class Movie_Recommender:
    """
    This class contains several methods to recommend movies on the app
    """
    movies_file = "ml-25m/movies.csv"
    ratings_file = "ml-25m/ratings.csv"
    links_file = "ml-25m/links.csv"
    tags_file = "ml-25m/tags.csv"
    # genome_scores = "ml-25m/genome-scores.csv"
    # genome_tags = "ml-25m/genome-tags.csv"

    # a list contain top-rated, most reviewed movie objects
    top_rating_movie_list = []
    most_reviewed_movie_list = []
    show_list = []
    # lists contain tag, rating objects
    tag_list = []
    movie_dict = {}

    def load_data(self):
        """
        This function will load all 25m data we have and create objects of different classes
        """

        # 1. movies data & links data
        movies = pd.read_csv(self.movies_file)
        links = pd.read_csv(self.links_file)
        # merge two datasets together
        movie_links = pd.merge(movies, links, how='left', on='movieId')

        # for each row:
        for r in range(movie_links.shape[0]):
            # create a movie object
            movie = Movie(movie_links.iloc[r, 0], movie_links.iloc[r, 1], movie_links.iloc[r, 2], movie_links.iloc[r, 3], movie_links.iloc[r,4])
            self.movie_dict[movie.movie_id] = movie

        print("Movies data loaded!")

        # 2. ratings data
        ratings = pd.read_csv(self.ratings_file)
        for r in range(ratings.shape[0]):
            Rating(ratings.iloc[r, 0], ratings.iloc[r, 1], ratings.iloc[r, 2], ratings.iloc[r, 3])
        print("Ratings data loaded!")

        # 3. tags data
        tags = pd.read_csv(self.tags_file)
        for r in range(tags.shape[0]):
            Tag(tags.iloc[r, 0], tags.iloc[r, 1], tags.iloc[r, 2], tags.iloc[r, 3])
        print("Tags data loaded!")

    # search by name or tag
    @classmethod
    def search_name_tag(cls, search_input):
        """
        This function will return the result of searching for a keyword in name or a tag
        :param search_input: name or tag
        :return: a list of top 6 (or less than 6) relevant movies
        """
        movie_output = []
        search_input_lower = search_input.lower()

        # name
        for movie in cls.movie_dict.values():
            if search_input_lower in movie.title.lower() or search_input_lower.strip() in movie.title.lower().strip() or search_input_lower.replace(" ", "") in movie.title.lower().replace(" ", ""):
                movie_output.append(movie)

        # then search tag
        for tag, movie_id_list in Tag.tag_movie.items():
            if search_input_lower == tag.lower() or search_input_lower.strip() == tag.lower() or search_input_lower.replace(" ", "") == tag.lower().replace(" ", ""):
                # each movie under the tag
                for id in movie_id_list:
                    try:
                        movie_output.append(cls.movie_dict[id])
                    except KeyError:
                        pass

        # if the result matching greater than 6, pick the one from name matching first
        if len(movie_output) > 6:
            movie_output = movie_output[:6]

        return movie_output

    @classmethod
    def set_movie_dict(cls, movie_dict):
        cls.movie_dict = movie_dict

    @classmethod
    def top_rating_movies(cls):
        """
        This function will randomly pick 6 top-rated movies
        :return: top rated movies
        """
        weighted_rating = Rating.calc_weighted_rating()
        print(len(cls.movie_dict))
        for movie in cls.movie_dict.values():
            movie.set_movie_weighted_rating(weighted_rating)
            movie_weighted_rating = movie.get_movie_weighted_rating()

            # we can define top-rated movie as movies with weighted score 4.5 and 5.0
            if 5.0 >= movie_weighted_rating >= 4.0:
                cls.top_rating_movie_list.append(movie)

        # choose 6 movies first
        random_top_rated = random.sample(cls.top_rating_movie_list, 6)

        max_length = 0
        for movie in random_top_rated:
            # append movies
            cls.show_list.append(movie)
            if len(movie.title) >= max_length:
                max_length = len(movie.title)

        Movie.title_max_length = max_length
        return random_top_rated

    @classmethod
    def popular_movie(cls, top_list):
        """
        This function will randomly pick 6 popular movies based on the number of review
        :return: 6 movies with top number of views
        """
        vote = Rating.calc_movie_vote_count()
        n_review_list = []
        for movie in cls.movie_dict.values():
            movie.set_movie_vote(vote)
            movie_vote = movie.get_movie_vote()

            # movie that are not in top_rated list and above 3.5:
            if movie not in top_list and movie.movie_weighted_rating > 3.5:
                n_review_list.append({'movie_object': movie, 'movie_votes': movie_vote})

        df = pd.DataFrame(n_review_list)
        sorted_df = df.sort_values('movie_votes', ascending=False)

        # get the first 100 most_voted movie
        first_100 = sorted_df.iloc[:100, :]
        random_index = random.sample(range(100), 6)

        # append movies to most_reviewed_movie_list
        for index in random_index:
            cls.most_reviewed_movie_list.append(first_100.iloc[index, 0])

        max_length = 0
        for movie in cls.most_reviewed_movie_list:
            cls.show_list.append(movie)
            if len(movie.title) >= max_length:
                max_length = len(movie.title)

        Movie.title_max_length = max_length
        return cls.most_reviewed_movie_list

    @classmethod
    def action(cls):
        """
        This function will randomly pick 6 action movie
        :return: 6 action movies
        """
        action_list = []

        # check "action" in genre
        for movie in cls.movie_dict.values():
            if "Action" in movie.genres_list and movie.movie_weighted_rating > 3.5:
                action_list.append(movie)

        # randomly select 20 first
        random_action = random.sample(action_list, 20)

        max_length = 0
        random_list = []
        count = 0
        for movie in random_action:
            if count <= 6 and movie not in cls.show_list:
                cls.show_list.append(movie)
                random_list.append(movie)
                count += 1
                if len(movie.title) >= max_length:
                    max_length = len(movie.title)

        Movie.title_max_length = max_length
        return random_list

    @classmethod
    def comedy(cls):
        """
        This function will randomly pick 6 comedy movie
        :return: 6 comedies movies
        """
        # check genre and weighted rating
        comedy_list = []
        for movie in cls.movie_dict.values():
            if "Comedy" in movie.genres_list and movie.movie_weighted_rating > 3.5:
                comedy_list.append(movie)

        # randomly select 20 first
        random_comedy = random.sample(comedy_list, 20)

        max_length = 0
        random_list = []
        count = 0
        for movie in random_comedy:
            if count <= 6 and movie not in cls.show_list:
                cls.show_list.append(movie)
                random_list.append(movie)
                count += 1
                if len(movie.title) >= max_length:
                    max_length = len(movie.title)

        Movie.title_max_length = max_length
        return random_list

    # similar here for adventure
    @classmethod
    def adventure(cls):
        """
        This function will randomly pick 6 adventure movie
        :return: 6 adventure movies
        """
        adventure_list = []
        for movie in cls.movie_dict.values():
            if "Adventure" in movie.genres_list and movie.movie_weighted_rating > 3.5:
                adventure_list.append(movie)

        random_adventure = random.sample(adventure_list, 20)

        max_length = 0
        random_list = []
        count = 0
        for movie in random_adventure:
            if count <= 6 and movie not in cls.show_list:
                cls.show_list.append(movie)
                random_list.append(movie)
                count += 1
                if len(movie.title) >= max_length:
                    max_length = len(movie.title)

        Movie.title_max_length = max_length
        return random_list

    # similar for dramas
    @classmethod
    def dramas(cls):
        """
        This function will randomly pick 6 dramas movie
        :return: 6 dramas movies
        """
        dramas_list = []
        for movie in cls.movie_dict.values():
            if "Drama" in movie.genres_list and movie.movie_weighted_rating > 3.5:
                dramas_list.append(movie)

        random_dramas = random.sample(dramas_list, 20)

        max_length = 0
        random_list = []
        count = 0
        for movie in random_dramas:
            if count <= 6 and movie not in cls.show_list:
                cls.show_list.append(movie)
                random_list.append(movie)
                count += 1
                if len(movie.title) >= max_length:
                    max_length = len(movie.title)

        Movie.title_max_length = max_length
        return random_list
