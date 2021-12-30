# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# Part of the code is quoted from BUS216 Professor Namini's class notes

# import libraries
import numpy as np
from datetime import datetime


class Rating:
    """
    This class stores ratings given by users (to specific movies)
    """
    user_rating = {}
    user_avg_rating = {}

    movie_rating = {}
    movie_avg_rating = {}

    movie_vote_count = {}
    weighted_rating = {}

    def __init__(self, user_id, movie_id, rating, timestamp):
        """
        This is the constructor of the rating class
        :param user_id: user identifier
        :param movie_id: movie identifier
        :param rating: user rating (one user may have ratings to different movies)
        :param timestamp: timestamp of recorded rating
        """

        self.user_id = str(user_id)
        self.movie_id = str(movie_id)
        self.rating = rating
        self.timestamp = timestamp
        self.time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self.weighted_rating = 0

        #         """
        #         After each time we create an object, the below code will update the class attribute user_rating dict
        #         Our output below will be like {user 1: [5, 4.5, 3, ...], user 2: [4, 4, 5, ...]}
        #         """
        #         if self.user_id not in Rating.user_rating.keys():
        #             Rating.user_rating[self.user_id] = []
        #         Rating.user_rating[self.user_id].append(self.rating)

        """
        After each time we create an object, the below code will update the class attribute user_rating dict
        Our output below will be like {Movie 1: [5, 4.5, 4, ...], Movie 2: [4.5, 4.5, 5, ...]}
        """
        if self.movie_id not in Rating.movie_rating.keys():
            Rating.movie_rating[self.movie_id] = []
        Rating.movie_rating[self.movie_id].append(self.rating)

    # if a movie does not have any rating, we remove it from movie object list
    @classmethod
    def delete_no_rating_movie_obj(cls, movie_recommender):
        movie_dict_old = movie_recommender.movie_dict
        movie_dict_new = {}
        for movie in movie_dict_old.values():
            if movie.movie_id in cls.movie_rating.keys():
                movie_dict_new[movie.movie_id] = movie
        movie_recommender.set_movie_dict(movie_dict_new)

    #     @classmethod
    #     def calc_user_avg_rating(cls):
    #         """
    #         This method will calculate the average score from a specific user
    #         :return: return a dict containing user_id and avg score that one user gives
    #         """
    #         for user_id in cls.user_rating.keys():
    #             rating_avg = round(sum(cls.user_rating[user_id])/len(cls.user_rating[user_id]), 3)
    #             Rating.user_avg_rating[user_id] = rating_avg
    #         return Rating.user_avg_rating

    @classmethod
    def calc_movie_vote_count(cls):
        """
        This method will calculate the average rating for a specific movie
        :return: a dict containing movie_id and avg score that all uses give
        """
        for movie_id in cls.movie_rating.keys():
            vote = len(cls.movie_rating[movie_id])
            Rating.movie_vote_count[movie_id] = vote
        return Rating.movie_vote_count

    @classmethod
    def calc_movie_avg_rating(cls):
        """
        This method will calculate the average rating for a specific movie
        :return: a dict containing movie_id and avg score that all uses give
        """
        for movie_id in cls.movie_rating.keys():
            rating_avg = round(sum(cls.movie_rating[movie_id]) / len(cls.movie_rating[movie_id]), 3)
            Rating.movie_avg_rating[movie_id] = rating_avg
        return Rating.movie_avg_rating

    @classmethod
    def calc_weighted_rating(cls):
        """
        Sources: https://medium.com/@developeraritro/building-a-recommendation-system-using-weighted-hybrid-technique-75598b6be8ed
        :return: a weighted average rating
        """

        # calc C: average of all movies
        all_avg = []
        for v in cls.calc_movie_avg_rating().values():
            all_avg.append(v)
        all_avg = np.array(all_avg)
        C = round(all_avg.mean(), 3)

        # calc m: minimum votes required to be listed (here we choose 0.7 quantile)
        all_vote = []
        for v in cls.calc_movie_vote_count().values():
            all_vote.append(v)
        all_vote = np.array(all_vote)
        m = np.quantile(all_vote, 0.7)
        vote = cls.calc_movie_vote_count()
        rating = cls.calc_movie_avg_rating()

        for movie_id in cls.movie_rating.keys():
            v = vote[movie_id]
            R = rating[movie_id]

            weighted_avg = ((R * v) + (C * m)) / (v + m)
            Rating.weighted_rating[movie_id] = round(weighted_avg, 2)

        return Rating.weighted_rating

    def __str__(self):
        return "User " + self.user_id + " -> " + self.movie_id + ": " + self.rating + "; " + self.timestamp

