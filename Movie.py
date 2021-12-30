# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# Part of the code is quoted from BUS216 Professor Namini's class notes

import json
import textwrap
from dash import dcc
from dash import html
import requests as re
from bs4 import BeautifulSoup


class Movie:
    """
    This class stores movie information
    """
    movie_vote = 0
    movie_avg_rating = 0
    movie_weighted_rating = 0
    title_max_length = 0

    def __init__(self, movie_id, title, genres, imdb_id, tmdb_id):
        """
        This is a constructor of the movie class
        :param movie_id: unique movie identifier
        :param title: tile of the movie
        :param genres: the genre of movie; in a format of g1|g2|g3...
        :param imdb_id: for individual movie links
        """
        self.movie_id = str(movie_id)
        self.title = title
        self.genres = genres

        # genre_list will split the genres field and turn it into a list
        self.genres_list = genres.split("|")
        self.movielens_link = "https://movielens.org/movies/{}".format(movie_id)

        # We will use imdb link not tmdb link here because there are some na values in tmdb
        # In order to get imdb_link, we can use the links.csv
        self.link = "http://www.imdb.com/title/tt0{}/".format(imdb_id)
        self.tmdb_id = tmdb_id

        self.picture_address = ""

    #     def get_movie_avg_rating(self, avg_rating_list):
    #         # Get average rating of each movie
    #         self.movie_avg_rating = avg_rating[self.movie_id]

    def set_movie_weighted_rating(self, weighted_rating_dict):
        self.movie_weighted_rating = weighted_rating_dict[self.movie_id]

    def get_movie_weighted_rating(self):
        return self.movie_weighted_rating

    def set_movie_vote(self, vote_dict):
        self.movie_vote = vote_dict[self.movie_id]

    def get_movie_vote(self):
        return self.movie_vote

    def draw_movie_block(self):
        title = self.title.ljust(self.title_max_length)
        movie_title_wrapped = textwrap.fill(title, 22, drop_whitespace=False)
        api_key = 'cc558b329bd33e01999187d615e4c9d7'
        endpoint = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(self.tmdb_id, api_key)

        try:
            r = re.get(endpoint)

            # use tmdb API to get the picture path:
            content = r.json()
            picture = content['poster_path']
            self.picture_address = 'https://image.tmdb.org/t/p/w500/{}'.format(picture)

        # if not exist, use try the imdb scraping
        except KeyError:
            try:
                page = re.get(self.link)
                soup = BeautifulSoup(page.content, "html.parser")
                self.picture_address = soup.find_all("img")[0]["src"]

            # if imdb picture source also cannot find:
            except IndexError:
                self.picture_address = 'https://static.wikia.nocookie.net/ideas/images/e/e4/Movie_night.jpg/revision/latest?cb=20141222232947'

        # we need it only when the imdb link not work:
        if re.get(self.link).status_code == 404:
            self.link = "https://www.themoviedb.org/movie/{}".format(self.tmdb_id)

        return (dcc.Link(href=self.link,
                         target='_blank',
                         children=[
                             # here we just want a shape of button:
                             html.Button(
                                 id='movie_{}'.format(self.movie_id),
                                 children=[
                                     # movie pic
                                     html.Img(
                                         src=self.picture_address,
                                         style={
                                             'height': '250px',
                                             'width': '200px'
                                         }
                                     ),

                                     html.Div("", style={'paddingTop': '1px'}),

                                     # movie text
                                     html.Div(html.P([movie_title_wrapped],
                                                     id="title_movie_{}".format(self.movie_id),
                                                     style={'whiteSpace': 'pre-wrap',
                                                            'textAlign': 'left'})),

                                     # movie rating
                                     html.Div("⭑{}".format(self.movie_weighted_rating),  # self.movie_avg_rating
                                              id="rating_movie_{}".format(self.movie_id),
                                              style={'textAlign': 'left'})
                                 ], style={
                                     'fontSize': 15,
                                     'backgroundColor': '#FFECE3',
                                     'paddingTop': '8px',
                                     'paddingBottom': '10px',
                                     'font-weight': 'bold',
                                     'font-family': 'monospace',
                                     'color': 'dimgrey',
                                 })
                         ], style={
                'backgroundColor': '##FFFCF7',
                'paddingBottom': '20px',
                'paddingRight': '5px'}))

    def __str__(self):
        return self.movie_id + ". " + self.title + " " + self.genres
