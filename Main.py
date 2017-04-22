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
            query = ("create table articles (ArticleID decimal(10,0), title varchar(256), img_url varchar(256), body text, score decimal(3,1));")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("create table UserArticles (ArticleID decimal(10,0), title varchar(256), img_url varchar(256), body text, score decimal(3,1));")
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

def getArticles():
    returnHTML = ""
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select ArticleID, title, img_url from articles")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    for a in cursor:
        returnHTML += "<div class='article_box'><a href='/Articles/%s'><img class='article_img' src='%s'><br>%s</a></div>" % (str(a['ArticleID']), str(a['img_url']),str(a['title']))
    if len(returnHTML) == 0:
        returnHTML = "There are no articles"   
    return returnHTML

def getUserArticles():
    returnHTML = ""
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select ArticleID, title, img_url from UserArticles")
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

def createReview(title, score, body, image):
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("insert into UserArticles (title, img_url, body, score) values (%s, %s, %s, %s)")
    cursor = connection.cursor()
    cursor.execute(query,(title, image, body, score))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)
    
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
    <p> </p> </body> </html>''' %(loginHTML)
    return pageContent

@app.route("/Articles/<articleID>")
def articleDetails(articleID):
    global linkList
    articleDetails = getArticleDetails(articleID)
    pageContent = commonHeader()
    pageContent += headBar("Articles")
    pageContent +='''</ul> </nav> <p>%s</p>''' % (articleDetails)
    return pageContent
    
@app.route("/Articles")
def articles():
    global linkList
    listArticles = getArticles()
    pageContent = commonHeader()
    pageContent += headBar("Articles")
    pageContent +='''</ul> </nav> <p>
    <form>
    <!--Creates a form-->
        <fieldset>
        <legend>Filter Reviews</legend>
        <!--Sets the title of the form-->
            <p>
                <label>Game Genre</label>
                <!--Labels the drop down box-->
                <select id = "myList">
                <!--Creates the list of things to display in the drop down box-->
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
                </select>
            </p>
        </fieldset>
    </form>
    </p>
    %s
    </body> </html>''' % (listArticles)
    return pageContent

@app.route("/CreateUserReview", methods = ['GET', 'POST'])
def createUserReviews():
    global linkList
    errorMessage = ""
    if request.method == 'POST':
        errorMessage = checkCreate(request.form['title'], request.form['score'], request.form['body'], request.form['image'])
        if errorMessage == "":
            createReview(request.form['title'], request.form['score'], request.form['body'], request.form['image'])
            return redirect(url_for('userReviews'))
    listUserArticles = getUserArticles()
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
            <button type="submit">Create</button>
            <!--Creates the create button-->
        </div>
    </form>
    %s
    </body> </html>
    ''' % (errorMessage)
    return pageContent
    
@app.route("/UserReviews")
def userReviews():
    global linkList
    listUserArticles = getUserArticles()
    pageContent = commonHeader()
    pageContent += headBar("User Reviews")
    pageContent +='''</ul> </nav> <p>
    <form>
    <!--Creates a form-->
        <fieldset>
        <legend>Filter Reviews</legend>
        <!--Sets the title of the form-->
            <p>
                <label>Game Genre</label>
                <!--Labels the drop down box-->
                <select id = "myList">
                <!--Creates the list of things to display in the drop down box-->
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
                </select>
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
    </body> </html>''' % (listUserArticles)
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
    <form>
    <!--Creates a form-->
        <fieldset>
        <legend>Filter Releases</legend>
        <!--Sets the title of the form-->
            <p>
                <label>Game Genre</label>
                <!--Labels the drop down box-->
                <select id = "myList">
                <!--Creates the list of things to display in the drop down box-->
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
                </select>
            </p>
        </fieldset>
    </form>
    </p> </body> </html>''' 
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
