from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations
from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# handler section -- indicates what code to execute based on the type of HTTP request that is sent to the server

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<a href = '/restaurants/new'>Make a New Restaurant </a></br></br>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/edit'>Edit  </a>" % restaurant.id
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br>"
                    output += "</br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += " <h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'> "
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'> " \
                              % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)


            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'> " \
                              % restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "</body></html>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to" \
                          " say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Holaaaa! <a href = '/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to" \
                          " say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # Create new Restaurant class
                newRestaurant = Restaurant(name= messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


        except:
            pass


# main() section -- instantiate our server and specify what port it will listen to

def main():
    '''
    the Python interpreter will try to attempt the code inside the try block,
    if a defined event occurs we can exit out of the code with an exception
    '''
    try:
        port = 8080
        server = HTTPServer(('',port), webServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever() # to keep HTTPServer constantly listening until we call Ctrl+C or exit the application

    # built-in exception that can be triggered when user holds Ctrl+C on the keyboard
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close() # shut down the server







# runs the main method when the Python interpreter executes the script
if __name__ == '__main__':
    main()