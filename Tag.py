# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li

# import libraries
from datetime import datetime


class Tag:
    tag_movie = {}
    """
    This class stores the tags attached to different movies
    """

    def __init__(self, user_id, movie_id, tag, timestamp):
        """
        This is the constructor for the Tag class
        :param user_id: unique user identifier
        :param movie_id: unique user identifier
        :param tag: one tag applied to one movie by one user
        :param timestamp: timestamp of recorded rating
        """

        self.user_id = user_id
        self.movie_id = movie_id
        self.tag = str(tag)
        self.timestamp = timestamp
        self.time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # We can have a dict like this {tag1: [movie1, movie2, ...], tag2: [movie1, movie2, ...]}
        if self.tag != "":
            if self.tag not in Tag.tag_movie.keys():
                Tag.tag_movie[self.tag] = []
            Tag.tag_movie[self.tag].append(movie_id)

    def __str__(self):
        return "User " + self.user_id + " -> " + self.movie_id + ": " + self.tag + "; " + self.timestamp
