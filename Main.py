
#Imports functions needed
from flask import Flask, request, url_for, redirect, make_response
from random import randint
from subprocess import call
import sys
import mysql.connector

app = Flask(__name__)

#Start-up function
@app.before_first_request
def createDatabase():
    try:
        connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    except:
        try:
            connection = mysql.connector.connect(user = "root", password = "Password1!")
            query = ("create database GameReview;")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("use GameReview;")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("create table UserDetails (username varchar(32), password varchar(32), cookie varchar(32));")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("create table articles (ArticleID mediumint not null auto_increment, title varchar(256), img_url varchar(256), body text, score decimal(3,1), genre decimal(2,0), PRIMARY KEY (ArticleID));")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("create table UserArticles (ArticleID mediumint not null auto_increment, title varchar(256), img_url varchar(256), body text, score decimal(3,1), genre decimal(2,0),PRIMARY KEY (ArticleID));")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("create table UpcomingReleases (title varchar(256), platforms varchar(256), date varchar(8));")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("commit;")
            cursor = connection.cursor()
            cursor.execute(query)
        except:
            print "Oh no"
            sys.exit(-1)

#Sets up the list of links that will be on the bar at the top
linkList = [["/","Home"],
            ["Articles","Articles"],
            ["UserReviews","User Reviews"],
            ["UpcomingReleases","Upcoming Releases"],
            ["Contact","Contact"],
            ["Login","Login"]#Left is the page that will be linked to, right is the label of the button
           ]

#Defines the function that will format the task bar at the top of the screen
def commonHeader():
    header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
	<link href="/static/styles.css" rel="stylesheet">
    </head>'''
    return header

#Defines the function that will set the title on each page 
def headBar(pageTitle):
    linkContent = ""
    for taskBar in linkList:
        linkContent += '<li class="menu_bar"><a class="menu_item" href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
    headText = '''<body>
    <h1>%s</h1>
    <!--Sets the title of the page-->
    %s
    <nav> <ul>''' % (pageTitle, linkContent)
    return headText

#Defines the function that checks the login details of a user against what is in the database
def checkLogin(username, password):
    #Connects to the GameReview database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select username from UserDetails where username = %s and password = %s")
    cursor = connection.cursor()
    #Searches for the username and password
    cursor.execute(query,(username, password))
    #Fetches the usernames and passwords from the database
    cursor.fetchall()
    if cursor.rowcount == 1:
        return True
    return False

#Defines the function that creates the cookie for the user that will keep them logged in
def secretNumber():
    returnNumber = ""
    for i in range(32):
        #Makes returnNumber be a random 32 digit number 
        returnNumber += str(randint(0,9))
    return returnNumber

#Defines the function that updates the user's cookie as they change screens
def updateUserCookie(username, secretNumber):
    #Connects to the GameReview database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("update UserDetails set cookie = %s where username = %s")
    cursor = connection.cursor()
    #Searches for the cookie in the database
    cursor.execute(query,(secretNumber, username))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

#Defines the function that will determine which user is logged in by looking at their cookie
def getUserBySecret(secretNumber):
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ('select username from UserDetails where cookie = "%s"' % (secretNumber))
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()
    if cursor.rowcount == 1:
        return True
    return False

def loginExists(username):
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ('select username from UserDetails where username = "%s"' % (username))
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()
    if cursor.rowcount > 0:
        return True
    return False

def storeAccount(username, password):
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("insert into UserDetails (username, password) values (%s, %s)")
    cursor = connection.cursor()
    cursor.execute(query,(username, password))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

def getArticles(genre):
    returnHTML = ""
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    whereStatement = ""
    if genre != None and genre != 0:
        whereStatement = "where genre = %s" % (genre)
    query = ("select ArticleID, title, img_url from articles %s" % (whereStatement))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    for a in cursor:
        returnHTML += "<div class='article_box'><a href='/Articles/%s'><img class='article_img' src='%s'><br>%s</a></div>" % (str(a['ArticleID']), str(a['img_url']),str(a['title']))
    if len(returnHTML) == 0:
        returnHTML = "There are no articles"   
    return returnHTML

def getUserArticles(genre):
    returnHTML = ""
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    whereStatement = ""
    if genre != None and genre != 0:
        whereStatement = "where genre = %s" % (genre)
    print "Where statement: %s" % (genre)
    query = ("select ArticleID, title, img_url from UserArticles %s" % (whereStatement))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    for a in cursor:
        returnHTML += "<div class='article_box'><a href='/UserReviews/%s'><img class='article_img' src='%s'><br>%s</a></div>" % (str(a['ArticleID']), str(a['img_url']),str(a['title']))
    if len(returnHTML) == 0:
        returnHTML = "There are no articles"   
    return returnHTML

def getArticleDetails(ArticleID):
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select ArticleID, title, img_url, body, score from articles where ArticleID = '%s'" % (ArticleID))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    for a in cursor:
        return "<h1>%s</h1><img src='%s'><p>%s</p><p>%s</p>" % (str(a['title']), str(a['img_url']), str(a['body']), str(a['score']))

def getUserArticleDetails(ArticleID):
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select ArticleID, title, img_url, body, score from UserArticles where ArticleID = '%s'" % (ArticleID))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    for a in cursor:
        return "<h1>%s</h1><img src='%s'><p>%s</p><p>%s</p>" % (str(a['title']), str(a['img_url']), str(a['body']), str(a['score']))

def checkCreate(title, score, body, image):
    if title == "":
        return "you must enter a title"
    if len(title)>256:
        return "title too long, cannot be more than 256 characters long"
    if score == "":
        return "you must enter a score"
    try:
        float(score)
    except:
        return "score must be a number"
    if float(score) >10 or float(score)<0:
        return "score (%s) must be between 0 and 10" % (score)
    if body == "":
        return "you must enter a body"
    if image == "":
        return "you must enter an image URL"
    if len(image) >256:
        return "Image url must beat most 256 characters long"
    return ""

def createReview(title, score, body, image, genre):
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("insert into UserArticles (title, img_url, body, score, genre) values (%s, %s, %s, %s, %s)")
    cursor = connection.cursor()
    cursor.execute(query,(title, image, body, score, genre))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

def getUpcoming():
    returnHTML = "<table><tr><td>Date</td><td>Title</td><td>Platforms</td></tr>"
    upcomingFound = False
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select title, platforms, date from upcomingreleases")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    for a in cursor:
        upcomingFound = True
        returnHTML += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a['date'], a['title'], a['platforms'])
    if upcomingFound == False:
        returnHTML = "There are no upcoming releases"
    return returnHTML

def genreList(submit):
    submitText = ""
    if submit == True:
        submitText = 'onchange="this.form.submit()"'
    return '''<label>Game Genre</label>
                <!--Labels the drop down box-->
                <select name="genre" id = "genre" %s>
                <!--Creates the list of things to display in the drop down box-->
                    <option value = "0">All</option>
                    <option value = "1">Action</option>
                    <option value = "2">Adventure</option>
                    <option value = "3">Indie</option>
                    <option value = "4">Strategy</option>
                    <option value = "5">Free to Play</option>
                    <option value = "6">Singleplayer</option>
                    <option value = "7">Multiplayer</option>
                    <option value = "8">Racing</option>
                    <option value = "9">FPS</option>
                    <option value = "10">Shooter</option>
                    <option value = "11">Co-op</option>
                </select>''' % (submitText)
    
@app.route("/")
def main():
    global linkList
    loginHTML = ""
    if 'secretNum' in request.cookies:
        secretNum = request.cookies.get('secretNum')
        if getUserBySecret(secretNum) == True:
            loginHTML = "user logged in"
    pageContent = commonHeader()
    pageContent += headBar("Fenrir")
    pageContent+= '''</ul> </nav> %s
    <p>Welcome to Fenrir, my computing coursework project.</p>
    <p>In order to view articles made by me, or another moderator, click on the articles tab.</p>
    <p>To view articles by users, or write your own article, click on the User Reviews tab.</p>
    <p>To view the upcoming releases, click on the upcoming releases tab.</p>
    <p>If you need to contact me, click on the contact tab and you will be able to email me.</p>
    <p>To login or create an account, click on the login tab.</p>
    <p>Thankyou for visiting Fenrir.</p>
    </body> </html>''' %(loginHTML)
    return pageContent

@app.route("/Articles/<articleID>")
def articleDetails(articleID):
    global linkList
    articleDetails = getArticleDetails(articleID)
    pageContent = commonHeader()
    pageContent += headBar("Articles")
    pageContent +='''</ul> </nav> <p>%s</p>''' % (articleDetails)
    return pageContent
    
@app.route("/Articles", methods = ['GET', 'POST'])
def articles():
    global linkList
    listArticles = getArticles(request.form.get('genre'))
    #if request.method=='POST':
     #   listArticles+="<BR>select = %s<BR>" % (request.form.get('genre'))
    pageContent = commonHeader()
    pageContent += headBar("Articles")
    pageContent +='''</ul> </nav> <p>
    <form action="/Articles" method="POST">
    <!--Creates a form-->
        <fieldset>
        <legend>Filter Reviews</legend>
        <!--Sets the title of the form-->
            <p>
                %s
            </p>
        </fieldset>
    </form>
    </p>
    %s
    </body> </html>''' % (genreList(True), listArticles)
    return pageContent

@app.route("/CreateUserReview", methods = ['GET', 'POST'])
def createUserReviews():
    global linkList
    errorMessage = ""
    if request.method == 'POST':
        errorMessage = checkCreate(request.form['title'], request.form['score'], request.form['body'], request.form['image'])
        if errorMessage == "":
            createReview(request.form['title'], request.form['score'], request.form['body'], request.form['image'], request.form['genre'])
            return redirect(url_for('userReviews'))
    listUserArticles = getUserArticles(request.form.get('genre'))
    pageContent = commonHeader()
    pageContent += headBar("Create a Review")
    pageContent +='''</ul> </nav> <p>
    </P>
    <form method=POST>
        <div class="container">
            <label><b>Title</b></label>
            <!--Labels the title box-->
            <input type="text" 
            placeholder="Enter Title" 
            name="title" 
            required>
            <label><b>Score</b></label>
            <!--Labels the score box-->
            <input type="text" 
            placeholder="Enter Score" 
            name="score" 
            required>
            <label><b>Body</b></label>
            <!--Labels the body box-->
            <input type="text" 
            placeholder="Enter Body" 
            name="body" 
            required>
            <label><b>Image</b></label>
            <!--Labels the image box-->
            <input type="text" 
            placeholder="Enter Image URL" 
            name="image" 
            required>
            <label><b>Genre</b></label>
            %s
            <button type="submit">Create</button>
            <!--Creates the create button-->
        </div>
    </form>
    %s
    </body> </html>
    ''' % (genreList(False), errorMessage)
    return pageContent
    
@app.route("/UserReviews", methods = ['GET', 'POST'])
def userReviews():
    global linkList
    print "Genre %s" % (request.form.get('genre'))
    listUserArticles = getUserArticles(request.form.get('genre'))
    pageContent = commonHeader()
    pageContent += headBar("User Reviews")
    pageContent +='''</ul> </nav> <p>
    <form action="/UserReviews" method="POST">
    <!--Creates a form-->
        <fieldset>
        <legend>Filter Reviews</legend>
        <!--Sets the title of the form-->
            <p>
                %s
            </p>
        </fieldset>
    </form>
    </p>
    <p>
    <form action="/CreateUserReview" method = GET>
    <button type="submit">Create article</button>
    </form>
    </p>
    %s
    </body> </html>''' % (genreList(True), listUserArticles)
    return pageContent

@app.route("/UserReviews/<articleID>")
def UserArticleDetails(articleID):
    global linkList
    articleDetails = getUserArticleDetails(articleID)
    pageContent = commonHeader()
    pageContent += headBar("User Reviews")
    pageContent +='''</ul> </nav> <p>%s</p>''' % (articleDetails)
    return pageContent

@app.route("/UpcomingReleases")
def upcomingReleases():
    pageContent = commonHeader()
    pageContent += headBar("Upcoming Releases")
    pageContent +='''</ul> </nav> <p>
    %s
    </p> </body> </html>''' % (getUpcoming())
    return pageContent

@app.route("/Contact")
def contact():
    pageContent = commonHeader()
    pageContent += headBar("Contact")
    pageContent +='''</ul> </nav>''' 
    return pageContent

@app.route("/Login", methods=['GET', 'POST'])
def login():
    falseLogin = ""
    if request.method == 'POST':
        if checkLogin(request.form['username'], request.form['password']):
            cookieNum = secretNumber()
            response = make_response(redirect(url_for("main")))
            response.set_cookie('secretNum', cookieNum)
            updateUserCookie(request.form["username"], cookieNum)
            return response
        falseLogin = "Your login details were incorrect"
    pageContent = commonHeader()
    pageContent += headBar("Login")
    pageContent +='''</ul> </nav> <p>
    </p>
    <form action="/Login" method = POST>
    <!--Creates the form for the login boxes-->
      <div class="container">
      <!--Creates a container to put the login boxes in-->
        <label style="color:red;">%s</label><br>
        <label><b>Username</b></label>
        <!--Labels the username box-->
        <input type="text" 
        placeholder="Enter Username" 
        name="username" 
        required>
        <!--[input type="text"] Sets the data type to text
        [placeholder="Enter Username"] sets the placeholder text to be "Enter Username" 
        [name="username"] names the box "username"
        [required] makes the data required-->

        <label><b>Password</b></label>
        <!--Labels the password box-->
        <input type="password" 
        placeholder="Enter Password" 
        name="password" 
        required>
        <!--[input type="password"] Sets the data type to password so it will be hidden
        [placeholder="Enter Password"] sets the placeholder text to be "Enter Password"
        [name="password"] names the box "password"
        [required] makes the data requires-->

        <button type="submit">Login</button>
        <!--Creates the login button-->
      </div>
    <p>
    </p>
      <div class="container" style="background-color:">
        <span class="psw">Don't have an account? <a href="/CreateAccount">Create one here</a></span>
        <!--Creates a link to the create account page for if a user does not yet have an account-->
      </div>
    </form> </body> </html>''' %(falseLogin)
    return pageContent

@app.route("/CreateAccount", methods=['GET', 'POST'])
def createAccount():
    falseCreate = ""
    if request.method == 'POST':
        if loginExists(request.form['username']):
            falseCreate = "username is already taken"
        else:
            if request.form['password1'] != request.form['password2']:
                falseCreate = "passwords do not match"
            else:
                storeAccount(request.form['username'], request.form['password1'])
                return(redirect(url_for("login")))
    pageContent = commonHeader()
    pageContent += headBar("Create Account")
    pageContent +='''</ul> </nav> <p>
    </p>
    <form action="/CreateAccount" method = POST>
    <!--Creates the form for the login boxes-->
      <div class="container">
      <!--Creates a container to put the login boxes in-->
        <label style="color:red;">%s</label><br>
        <label><b>Username</b></label>
        <!--Labels the username box-->
        <input type="text" 
        placeholder="Enter Username" 
        name="username" 
        required>
        <!--[input type="text"] Sets the data type to text
        [placeholder="Enter Username"] sets the placeholder text to be "Enter Username" 
        [name="username"] names the box "username"
        [required] makes the data required-->

        <label><b>Password</b></label>
        <!--Labels the password box-->
        <input type="password" 
        placeholder="Enter Password" 
        name="password1" 
        required>
        <!--[input type="password"] Sets the data type to password so it will be hidden
        [placeholder="Enter Password"] sets the placeholder text to be "Enter Password"
        [name="password1"] names the box "password1"
        [required] makes the data requires-->
                       
        <label><b>Repeat Password</b></label>
        <!--Labels the password box-->
        <input type="password" 
        placeholder="Enter Password" 
        name="password2" 
        required>
        <!--[input type="password"] Sets the data type to password so it will be hidden
        [placeholder="Enter Password"] sets the placeholder text to be "Enter Password"
        [name="password2"] names the box "password2"
        [required] makes the data requires-->

        <button type="submit">Create</button>
        <!--Creates the create button-->
      </div>
    <p>
    </p>
      <div class="container" style="background-color:">
        <span class="psw">Don't have an account? <a href="">Create one here</a></span>
        <!--Creates a link to the create account page for if a user does not yet have an account-->
      </div>
    </form> </body> </html>''' %(falseCreate)
    return pageContent
    
if __name__ == "__main__":
    app.run()
