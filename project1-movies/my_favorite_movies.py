import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <link href="https://fonts.googleapis.com/css?family=Gruppo" rel="stylesheet">
    <link rel="icon" type="image/png" href="C:\Development\Movies\project1/favicon-32x32.png" sizes="32x32" />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Favorite Movies!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            background-color: #333333;
            padding-top:130px;
        }
        .website-title {
            position: relative;
            top: 30%; left: 6%;
            transform: translate(0%,0%);
            line-height:100%;
            font-size: 45px;
            font-weight: bold;
            font-family: 'Gruppo', cursive;
            color: #72009A;
            text-shadow: 5px 5px 10px black;
        }
        .movie-title {
            color: #a7e71f;
            font-family: 'Gruppo', cursive;
            font-size: 30px;
            font-weight: bold;

        }
        .container {
            margin-top:21.6667px;
        }
        .top-image {
            height: 120px;
            background-image: url("http://cdn.wonderfulengineering.com/wp-content/uploads/2014/09/Green-Wallpaper-1.jpg");
            background-size: cover;
            background-position: 100% 60%;
            background-repeat: no-repeat;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 1024px;
            height: 768px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
            position: relative;
        }
         .logo {
            align: center;
            vertical-align: middle;
        }
        .movie-tile .movie-poster-image{
            border-radius: 5px;
            opacity: 1.0;
        }
        .movie-tile:hover .movie-poster-image{
            border-radius: 5px;
            opacity: 0.2;
        }
        .movie-tile .outter{
            position: relative;
        }
        .whitebg {
            background-color: #a7e71f;
            height: 342px;
            width: 220px;
            position: absolute;
            top: 0%; left: 50%;
            transform: translate(-50%,0%);
            margin-top: 20px;
            border-radius: 5px;
            opacity: 0.8;
        }
        .movie-tile .col{
            position: absolute;
            top: 0%; left: 50%;
            transform: translate(-50%,0%);
            height: 342px;
            visibility:hidden;
            overflow: hidden;
        }
        .movie-tile:hover .col{
            height: 342px;
            position: absolute;
            top: 0%; left: 50%;
            transform: translate(-50%,0%);
            visibility: visible;
            overflow: hidden;
        }
        .movie-tile .storyline_text{
            position: absolute;
            top: 0%; left: 50%;
            transform: translate(-50%,0%);
            width: 200px;
            text-align: center;
            margin-top: 10px;
            color:   #75089A;
            font-size: 24px;
            font-family: 'Gruppo', cursive;
            font-weight: bold;
            line-height: 2.3ex;
        }
         .outter .click-to-watch {
            position: absolute;
            top: 70%; left: 20%;
            transform: translate(-50%,0%);
            visibility: hidden;
            overflow: hidden;
        }
        .outter:hover .click-to-watch {
            position: absolute;
            top: 78%; left: 50%;
            width: 200px;
            visibility: visible;
            visibility: visible;
            overflow: hidden;
            line-height: 2.2ex;
            color:   #333333;
            font-size: 19px;
            font-family: 'Gruppo', cursive;
            font-weight: bold;
            text-decoration: underline;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe ></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog" >
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
      <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top top-image" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="website-title" href="#">My Favorite Movies</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-4 col-lg-4 col-sm-6 col-xs-12 movie-tile text-center " data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
  <div class = "whitebg"></div>
    <div class="outter">
      <img class="movie-poster-image" src="{poster_image_url}" width="220" height="342">
        <div class="col-sm-10 col-xs-12 col">
            <p class="storyline_text">{storyline}</p>
        </div>
      <h2 class="movie-title">{movie_title}</h2>
      <p class="click-to-watch">Click to watch trailer</p>
  </div>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            storyline=movie.storyline,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id

        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('my_favorite_movies.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(
      movie_tiles=create_movie_tiles_content(movies)
  )
  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible