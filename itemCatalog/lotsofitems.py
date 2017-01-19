from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# items for Soccer
category1 = Category(user_id=1, name="Soccer")
session.add(category1)
session.commit()

Item1 = Item(user_id=1, name="Jersey", description="a loose shirt worn by a member of a sports team as part of a uniform",
                      category=category1)
session.add(Item1)
session.commit()


Item2 = Item(user_id=1, name="Shin guards", description="a protective covering, usually of leather or plastic and often "
                                                        "padded, for the shins and sometimes the knees, worn chiefly by "
                                                        "catchers in baseball and goalkeepers in ice hockey.",
             category=category1)
session.add(Item2)
session.commit()



# items for Snowboarding
category2 = Category(user_id=1, name="Snowboarding")
session.add(category2)
session.commit()


Item1 = Item(user_id=1, name="Snowboard", description="a board for gliding on snow, resembling a wide ski, to which both"
                                                      " feet are secured and that one rides in an upright position.",
             category=category2)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Goggles", description="large spectacles equipped with special lenses, protective rims, "
                                                    "etc., to prevent injury to the eyes from strong wind, flying "
                                                    "objects, blinding light, etc.",
             category=category2)
session.add(Item2)
session.commit()




print "added items!"