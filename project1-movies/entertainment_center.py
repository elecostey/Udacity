import media
import my_favorite_movies

# mock the movie data:
gladiator = media.Movie("Gladiator",
                        "When a Roman general is betrayed and his family "
                        "murdered by an emperor's corrupt son, he comes to "
                        "Rome as a gladiator to seek revenge.",
                        "http://www.impawards.com/2000/posters/gladiator_ver3_xlg.jpg",
                        "https://www.youtube.com/watch?v=0BLZbrLogTo")


armageddon = media.Movie("Armageddon",
                         "After discovering that an asteroid the size of Texas"
                         " is going to impact Earth in less than a month, "
                         "N.A.S.A. recruits a misfit team of deep core "
                         "drillers to save the planet.",
                         "https://www.movieposter.com/posters/archive/main/63/MPW-31982",
                         "https://www.youtube.com/watch?v=kg_jH47u480")

the_dark_knight = media.Movie("The Dark Knight",
                              "When the menace known as the Joker wreaks havoc"
                              " and chaos on the people of Gotham, the caped "
                              "crusader must come to terms with one of the "
                              "greatest psychological tests of his ability to "
                              "fight injustice.",
                              "https://paulmmartinblog.files.wordpress.com/2011/07/the_dark_knight_poster.jpg",
                              "https://www.youtube.com/watch?v=5y2szViJlaY")

world_war_z = media.Movie("World War Z",
                          "Former United Nations employee Gerry Lane traverses"
                          " the world in a race against time to stop the "
                          "Zombie pandemic that is toppling armies and "
                          "governments, and threatening to destroy humanity "
                          "itself.",
                          "http://cdn.collider.com/wp-content/uploads/world-war-z-poster-3.jpg",
                          "https://www.youtube.com/watch?v=Md6Dvxdr0AQ")

seven_pounds = media.Movie("Seven Pounds",
                           "A man with a fateful secret embarks on an "
                           "extraordinary journey of redemption by forever "
                           "changing the lives of seven strangers.",
                           "http://www.firstshowing.net/img2/sevenpounds-willsmith-poster-full.jpg",
                           "https://www.youtube.com/watch?v=kitjcYHMRoQ")

troy = media.Movie("Troy",
                   "An adaptation of Homer's great epic, the film follows the "
                   "assault on Troy by the united Greek forces and chronicles "
                   "the fates of the men involved.",
                   "http://www.impawards.com/2004/posters/troy_ver7.jpg",
                   "https://www.youtube.com/watch?v=znTLzRJimeY")

# appending movies into a list:
movies = [gladiator, armageddon, troy, the_dark_knight, world_war_z, seven_pounds]

# calling the external rendering function:
my_favorite_movies.open_movies_page(movies)
