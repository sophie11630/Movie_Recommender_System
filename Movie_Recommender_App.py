# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li

# import other libraries
import dash
from dash import html
from dash import dcc
from Rating import Rating
from Movie_Recommender import Movie_Recommender
from dash.dependencies import Input, Output, State


# find movies that will be shown
def selected_movies(movie_recommender):
    top_list = movie_recommender.top_rating_movies()
    popular_list = movie_recommender.popular_movie(top_list)
    action_list = movie_recommender.action()
    comedy_list = movie_recommender.comedy()
    adventure_list = movie_recommender.adventure()
    drama_list = movie_recommender.dramas()
    return [top_list, popular_list, action_list, comedy_list, adventure_list, drama_list]


def movie_recommendation_app(movie_recommender):
    select = selected_movies(movie_recommender)
    top_list = select[0]
    popular_list = select[1]
    action_list = select[2]
    comedy_list = select[3]
    adventure_list = select[4]
    drama_list = select[5]

    # log-in authorization
    #     USERNAME_PASSWORD_PAIRS = [['username', 'password'], ['movierecommender','bus216']]

    app = dash.Dash()
    server = app.server
    #     auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

    app.layout = html.Div(children=[
        # 1. first block with tile
        html.Div([
            html.Div("Movie Recommender System",
                     style={
                         'textAlign': 'center',
                         'color': "Cornflowerblue",
                         'fontSize': '32px',
                         'fontWeight': 'bold',
                         'font-family': 'monospace',
                         'backgroundColor': '#D0E1F5'
                     }),
            html.H1("", style={'backgroundColor': '#D0E1F5'})
        ], style={'backgroundColor': '#D0E1F5'}),

        # 2. contains a search engine
        html.Div([
            # 2.1
            dcc.Link('Data Source: Movielens', href='https://grouplens.org/datasets/movielens/',
                     target='_blank',
                     style={
                         'color': 'Cornflowerblue',
                         'font-size': '18px',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'display': 'inline-block',
                         'paddingLeft': '6px',
                         'paddingRight': '25px'
                     }),
            # 2.2
            dcc.Input(id="search",
                      value="",
                      type='text',
                      style={'width': '50%',
                             'size': '20',
                             'height': '30px',
                             'font-size': '16px',
                             'font-family': 'monospace',
                             'display': 'inline-block',
                             'paddingRight': '20px'}),
            # 2.3 add a clickable element
            html.Div([
                html.Button(
                    id='submit_button',
                    n_clicks=0,
                    children='🔍',
                    style={'font-size': 24,
                           'font-family': 'arial',
                           'verticalAlign': 'top'}
                ),
            ], style={'display': 'inline-block'})
        ], style={'backgroundColor': '#D0E1F5'}),

        # 2.4 add a block to show search results
        html.Div([
            html.Div(children=[
            ], id='search_result',
                style={
                    'backgroundColor': '#E8FFFD',
                    'paddingTop': '10px',
                    'paddingBottom': '5px',
                    'paddingRight': '5px',
                    'paddingLeft': '10px',
                    'height': '400px',
                    'marginLeft': '20px',
                    'marginRight': '20px'
                })
        ], style={
            'backgroundColor': '#D0E1F5',
            'paddingBottom': '10px',
        }),
        # a break line
        html.Div(" ", style={'backgroundColor': 'pink', 'paddingTop': '8px'}),

        # 3. Top Rated Movies
        html.Div([
            html.Div("📀 Top Rated",
                     style={
                         'color': 'dimgrey',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'fontSize': '20px',
                         'paddingRight': '15px',
                         'paddingTop': '10px',
                         'paddingBottom': '2px'
                     }),
            html.Div([
                # add movie block
                top_list[0].draw_movie_block(),
                top_list[1].draw_movie_block(),
                top_list[2].draw_movie_block(),
                top_list[3].draw_movie_block(),
                top_list[4].draw_movie_block(),
                top_list[5].draw_movie_block()
            ], style={
                'backgroundColor': '#FFFCF7',
                'display': 'in-line'
            })

        ], style={
            'backgroundColor': '#FFFCF7',
            'paddingTop': '2px',
            'paddingBottom': '20px',
            'paddingRight': '5px',
            'display': 'in-line'}),

        # 4. Most Popular
        html.Div([
            html.Div("📀 Popular on MovieLens",
                     style={
                         'color': 'dimgrey',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'fontSize': '20px',
                         'paddingRight': '15px',
                         'paddingTop': '10px',
                         'paddingBottom': '2px'}
                     ),

            popular_list[0].draw_movie_block(),
            popular_list[1].draw_movie_block(),
            popular_list[2].draw_movie_block(),
            popular_list[3].draw_movie_block(),
            popular_list[4].draw_movie_block(),
            popular_list[5].draw_movie_block()

        ], style={
            'backgroundColor': '#FFFCF7',
            'paddingTop': '2px',
            'paddingRight': '5px',
            'paddingBottom': '20px'}),

        # 5. Romance Movie
        html.Div([
            html.Div("📀 Action Movies",
                     style={
                         'color': 'dimgrey',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'fontSize': '20px',
                         'paddingRight': '15px',
                         'paddingTop': '10px',
                         'paddingBottom': '2px'}
                     ),
            action_list[0].draw_movie_block(),
            action_list[1].draw_movie_block(),
            action_list[2].draw_movie_block(),
            action_list[3].draw_movie_block(),
            action_list[4].draw_movie_block(),
            action_list[5].draw_movie_block()
        ], style={
            'backgroundColor': '#FFFCF7',
            'paddingTop': '2px',
            'paddingBottom': '20px'}),

        # 6. Comedy Movie
        html.Div([
            html.Div("📀 Comedies",
                     style={
                         'color': 'dimgrey',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'fontSize': '20px',
                         'paddingRight': '15px',
                         'paddingTop': '10px',
                         'paddingBottom': '2px'}
                     ),
            comedy_list[0].draw_movie_block(),
            comedy_list[1].draw_movie_block(),
            comedy_list[2].draw_movie_block(),
            comedy_list[3].draw_movie_block(),
            comedy_list[4].draw_movie_block(),
            comedy_list[5].draw_movie_block()
        ], style={
            'backgroundColor': '#FFFCF7',
            'paddingTop': '2px',
            'paddingBottom': '20px'}),

        # 7. Adventure Movie
        html.Div([
            html.Div("📀 Adventure",
                     style={
                         'color': 'dimgrey',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'fontSize': '20px',
                         'paddingRight': '15px',
                         'paddingTop': '10px',
                         'paddingBottom': '2px'}
                     ),
            adventure_list[0].draw_movie_block(),
            adventure_list[1].draw_movie_block(),
            adventure_list[2].draw_movie_block(),
            adventure_list[3].draw_movie_block(),
            adventure_list[4].draw_movie_block(),
            adventure_list[5].draw_movie_block()
        ], style={
            'backgroundColor': '#FFFCF7',
            'paddingTop': '2px',
            'paddingBottom': '20px'}),

        # 8. Drama
        html.Div([
            html.Div("📀 Dramas",
                     style={
                         'color': 'dimgrey',
                         'font-weight': 'bold',
                         'font-family': 'monospace',
                         'fontSize': '20px',
                         'paddingRight': '15px',
                         'paddingTop': '10px',
                         'paddingBottom': '2px'}
                     ),
            drama_list[0].draw_movie_block(),
            drama_list[1].draw_movie_block(),
            drama_list[2].draw_movie_block(),
            drama_list[3].draw_movie_block(),
            drama_list[4].draw_movie_block(),
            drama_list[5].draw_movie_block()
        ], style={
            'backgroundColor': '#FFFCF7',
            'paddingTop': '2px',
            'paddingBottom': '20px'}),

    ], style={'backgroundColor': '#D0E1F5', 'paddingTop': '40px'})

    """
    add callbacks
    """

    # 1. search and button
    @app.callback(Output("search_result", "children"),
                  [Input("submit_button", "n_clicks")],
                  [State("search", "value")])
    def search_page(n_clicks, input_value):
        search_movie = Movie_Recommender.search_name_tag(input_value)
        if len(search_movie) == 1:
            return (
                search_movie[0].draw_movie_block()
            )
        elif len(search_movie) == 2:
            return (
                search_movie[0].draw_movie_block(),
                search_movie[1].draw_movie_block()
            )
        elif len(search_movie) == 3:
            return (
                search_movie[0].draw_movie_block(),
                search_movie[1].draw_movie_block(),
                search_movie[2].draw_movie_block()
            )
        elif len(search_movie) == 4:
            return (
                search_movie[0].draw_movie_block(),
                search_movie[1].draw_movie_block(),
                search_movie[2].draw_movie_block(),
                search_movie[3].draw_movie_block()
            )
        elif len(search_movie) == 5:
            return (
                search_movie[0].draw_movie_block(),
                search_movie[1].draw_movie_block(),
                search_movie[2].draw_movie_block(),
                search_movie[3].draw_movie_block(),
                search_movie[4].draw_movie_block()
            )
        elif len(search_movie) == 6:
            return (
                search_movie[0].draw_movie_block(),
                search_movie[1].draw_movie_block(),
                search_movie[2].draw_movie_block(),
                search_movie[3].draw_movie_block(),
                search_movie[4].draw_movie_block(),
                search_movie[5].draw_movie_block()
            )

    return app


def main():
    movie_recommender = Movie_Recommender()
    movie_recommender.load_data()
    Rating.delete_no_rating_movie_obj(movie_recommender)
    print(len(movie_recommender.movie_dict))

    app = movie_recommendation_app(movie_recommender)
    app.run_server(debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
