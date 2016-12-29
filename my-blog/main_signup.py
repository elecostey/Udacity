import os
import re
import random
import hashlib
import hmac
from string import letters
import time
import webapp2
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class PostDatabase(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)
    likes = db.IntegerProperty(required=False)
    unlikes = db.IntegerProperty(required=False)
    liked_by = db.ListProperty(int)
    unliked_by = db.ListProperty(int)

    def fetchUserName(self):
        user = User.by_id(self.user_id)
        return user.name

    def render(self):  # renderpost is used to render jinja templates
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", renderpost=self)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


class CommentDatabase(db.Model):
    post = db.ReferenceProperty(PostDatabase, required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    content = db.TextProperty(required=True)

    # get number of comments for a blog id
    @classmethod
    def count_by_blog_id(cls, blog_id):
        c = CommentDatabase.all().filter('post =', blog_id)
        return c.count()

    # get all comments for a specific blog id
    @classmethod
    def all_by_blog_id(cls, blog_id):
        c = db.GqlQuery("SELECT *"
                        " FROM CommentDatabase"
                        " WHERE post = :blog_id"
                        " ORDER BY created DESC"
                        " LIMIT 10", blog_id=blog_id)
        return c

    def fetchUserName(self):
        user = self.user
        return user.name

    def render(self):  # renderpost is used to render jinja templates
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", renderpost=self)


class Like(db.Model):
    post_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(User)


class Unlike(db.Model):
    post_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(User)


USER_RE = re.compile(r"[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)

secret = 'f5mpj2dh8'


# Cookie hashing

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

# Password hashing


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

# Grouping key for users


def users_key(group='default'):
    return db.Key.from_path('users', group)


class BlogHandler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def render_post(response, post_tool):
        response.out.write('<b>' + post_tool.subject + '</b><br>')
        response.out.write(post_tool.content)

    def render_comment(response, post_comment, user):
        response.out.write(post_comment.content)


class BlogFront(BlogHandler):
    def get(self):
        allposts = db.GqlQuery("SELECT *"
                               " FROM PostDatabase"
                               " ORDER BY created DESC"
                               " LIMIT 10")
        self.render('blog.html',
                    allposts=allposts)


class PostPage(BlogHandler):
    def get(self, post_id):
        if not self.user:
            return self.redirect('/login')
        key = db.Key.from_path('PostDatabase',
                               int(post_id),
                               parent=blog_key())
        post_tool = db.get(key)
        if not post_tool:
            self.error(404)
            return

        post = db.get(key)
        if not post:
            self.error(404)
            return

        all_comments = CommentDatabase.all_by_blog_id(post)
        comments_count = CommentDatabase.count_by_blog_id(post)

        self.render("permalink.html",
                    post_tool=post_tool,
                    all_comments=all_comments,
                    comments_count=comments_count)


class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else :
            self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect("/login")

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post_tool = PostDatabase(parent=blog_key(),
                                     user_id=self.user.key().id(),
                                     subject=subject,
                                     content=content,
                                     likes=0,
                                     unlikes=0,
                                     liked_by=[],
                                     unliked_by=[])
            post_tool.put()
            self.redirect('/blog/%s' % str(post_tool.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html",
                        subject=subject,
                        content=content,
                        error=error)


class EditPost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('PostDatabase',
                                   int(post_id),
                                   parent=blog_key())
            post_tool = db.get(key)
            # Check to see if the logged in user is the post's author
            if post_tool.user_id == self.user.key().id():
                self.render("editpost.html",
                            post_tool=post_tool,
                            subject=post_tool.subject,
                            content=post_tool.content,
                            post_id=post_id)

    def post(self, post_id):
        key = db.Key.from_path('PostDatabase',
                                   int(post_id),
                                   parent=blog_key())
        post_tool = db.get(key)
        # Check to see if the logged in user is the post's author
        if post_tool.user_id == self.user.key().id():
            if self.request.get("submit"):
                subject = self.request.get('subject')
                content = self.request.get('content')

                if subject and content:
                    key = db.Key.from_path('PostDatabase',
                                           int(post_id),
                                           parent=blog_key())
                    post_tool = db.get(key)
                    post_tool.subject = subject
                    post_tool.content = content

                    post_tool.put()

                    self.redirect('/blog/%s' % str(post_tool.key().id()))
                else:  # In case user tries to submit an empty edit form
                    error = "There must be a subject and content."
                    self.render("editpost.html",
                                post_tool=post_tool,
                                subject=post_tool.subject,
                                content=post_tool.content,
                                post_id=post_id,
                                error=error)

            elif self.request.get("cancel"):
                self.redirect('/blog/%s' % str(post_tool.key().id()))

        else:
            self.redirect('/blog/%s' % str(post_tool.key().id()))


class Delete(BlogHandler):
    def post(self, post_id):
        key = db.Key.from_path('PostDatabase',
                               int(post_id),
                               parent=blog_key())
        post_tool = db.get(key)
        # Check to see if the logged in user is the post's author
        if post_tool.user_id == self.user.key().id():
            key = db.Key.from_path('PostDatabase',
                                    int(post_id),
                                    parent=blog_key())
            db.delete(key)
            self.redirect('/success')

        else:
            self.redirect('/blog')


class LikePost(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            return self.redirect('/login')
        key = db.Key.from_path('PostDatabase',
                               int(post_id),
                               parent=blog_key())
        post_tool = db.get(key)
        user_id = post_tool.user_id
        logged_user = self.user.key().id()
        if user_id == logged_user or logged_user in post_tool.liked_by:
            self.redirect('/like_not_registered')

        elif user_id != logged_user:
            post_tool.likes += 1
            post_tool.liked_by.append(logged_user)
            post_tool.put()
            time.sleep(.5)
            self.redirect('/like_registered')


class UnlikePost(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            return self.redirect('/login')
        key = db.Key.from_path('PostDatabase',
                               int(post_id),
                               parent=blog_key())
        post_tool = db.get(key)
        user_id = post_tool.user_id
        logged_user = self.user.key().id()
        if user_id == logged_user or logged_user in post_tool.unliked_by:
            self.redirect('/unlike_not_registered')

        elif user_id != logged_user:
            post_tool.unlikes += 1
            post_tool.unliked_by.append(logged_user)
            post_tool.put()
            time.sleep(.5)
            self.redirect('/unlike_registered')


class Success(BlogHandler):
    def get(self):
        self.render('success.html', username=self.user.name)


class Success_like(BlogHandler):
    def get(self):
        self.render('like_registered.html', username=self.user.name)


class Unsuccess_like(BlogHandler):
    def get(self):
        self.render('like_not_registered.html', username=self.user.name)


class Success_unlike(BlogHandler):
    def get(self):
        self.render('unlike_registered.html', username=self.user.name)


class Unsuccess_unlike(BlogHandler):
    def get(self):
        self.render('unlike_not_registered.html', username=self.user.name)


class NewComment(BlogHandler):
    def get(self, post_id):
        if self.user:
            self.render("newcomment.html")
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            self.write("You must be logged in to make a new post.")

        key = db.Key.from_path('PostDatabase',
                               int(post_id),
                               parent=blog_key())
        post = db.get(key)
        # if the post does not exist throw a 404 error
        if not post:
            self.error(404)
            return

        content = self.request.get('content')
        comments_count = CommentDatabase.count_by_blog_id(post)

        if content:
            post_comment = CommentDatabase(post=post,
                                           user=self.user,
                                           comments_count=comments_count,
                                           content=content)

            post_comment.put()
            time.sleep(.5)
            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "content, please!"
            self.render("newcomment.html",
                        content=content,
                        error=error)


class EditComment(BlogHandler):

    def get(self, post_id, comment_id):
        comment = CommentDatabase.get_by_id(int(comment_id))

        if comment:

            if comment.user.name == self.user.name:
                self.render("editcomment.html", content=comment.content)

            else:
                error = "You cannot edit other user comments"
                self.render("editcomment.html", edit_error=error)

        else:
            error = "This comment no longer exists"
            self.render("editcomment.html", edit_error=error)

    def post(self, post_id, comment_id):
        if self.request.get("update_comment"):
            comment = CommentDatabase.get_by_id(int(comment_id))

            if comment.user.name == self.user.name:
                comment.content = self.request.get('content')
                comment.put()
                time.sleep(0.1)
                self.redirect('/blog/%s' % str(post_id))

            else:
                error = "You cannot edit other users' comments'"
                self.render(
                    "editcomment.html",
                    content=comment.content,
                    edit_error=error)

        elif self.request.get("cancel"):
            self.redirect('/blog/%s' % str(post_id))


class DeleteComment(BlogHandler):

    def post(self, post_id, comment_id):
        comment = CommentDatabase.get_by_id(int(comment_id))
        if comment:
                db.delete(comment)
                time.sleep(0.1)
                self.redirect('/blog/%s' % str(post_id))
        else:
            self.write("Comment not found!")


class Signup(BlogHandler):

    def get(self):
        self.render('signup_form.html')

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username, email=self.email)

        if len(self.username) == 0:
            params['error_username'] = "Please enter an username."
            have_error = True
        elif not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if len(self.password) == 0:
            params['error_password'] = "Please enter a password."
            have_error = True
        elif not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup_form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup_form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')


class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')


class WelcomeUser(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome_form.html', username=self.user.name)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/delete/([0-9]+)', Delete),
                               ('/success', Success),
                               ('/like_registered', Success_like),
                               ('/like_not_registered', Unsuccess_like),
                               ('/unlike_registered', Success_unlike),
                               ('/unlike_not_registered', Unsuccess_unlike),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/blog/unlike/([0-9]+)', UnlikePost),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/welcome', WelcomeUser),
                               ('/blog/newcomment/([0-9]+)', NewComment),
                               ('/blog/([0-9]+)/removecomment/([0-9]+)',
                                DeleteComment),
                               ('/blog/([0-9]+)/editcomment/([0-9]+)',
                                EditComment)],
                              debug=True)
