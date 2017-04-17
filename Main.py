from flask import Flask, request, url_for, redirect, make_response
from random import randint
import mysql.connector

app = Flask(__name__)

linkList = [["/","Home"],
            ["Articles","Articles"],
            ["UserReviews","User Reviews"],
            ["UpcomingReleases","Upcoming Releases"],
            ["Contact","Contact"],
            ["Login","Login"]
           ]

def commonHeader():
    header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <style>
    li { list-style-type: none; padding: 0; margin: 0; background-color: #8E44AD; } li { display: inline-block; } li a { display: block; padding: 10px; color: #FDFEFE; } li a:hover { background-color: #BB8FCE; } </style> 
    <!--Formats the main bar at the top of the screen--> 
    </style>
    </head>'''
    return header

def headBar(pageTitle):
    linkContent = ""
    for taskBar in linkList:
        linkContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
    headText = '''<body>
    <h1>%s</h1>
    <!--Sets the title of the page-->
    %s
    <nav> <ul>''' % (pageTitle, linkContent)
    return headText

def checkLogin(username, password):
    connection = mysql.connector.connect(user = "root", password = "Password", database = "UserDetails")
    query = ("select username from UserDetails where username = %s and password = %s")
    cursor = connection.cursor()
    cursor.execute(query,(username, password))
    cursor.fetchall()
    if cursor.rowcount == 1:
        return True
    return False

def secretNumber():
    returnNumber = ""
    for i in range(32):
        returnNumber += str(randint(0,9))
    return returnNumber

def updateUserCookie(username, secretNumber):
    connection = mysql.connector.connect(user = "root", password = "Password", database = "UserDetails")
    query = ("update UserDetails set cookie = %s where username = %s")
    cursor = connection.cursor()
    cursor.execute(query,(secretNumber, username))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

def getUserBySecret(secretNumber):
    connection = mysql.connector.connect(user = "root", password = "Password", database = "UserDetails")
    query = ('select username from UserDetails where cookie = "%s"' % (secretNumber))
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()
    if cursor.rowcount == 1:
        return True
    return False

def loginExists(username):
    connection = mysql.connector.connect(user = "root", password = "Password", database = "UserDetails")
    query = ('select username from UserDetails where username = "%s"' % (username))
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()
    if cursor.rowcount > 0:
        return True
    return False

def storeAccount(username, password):
    connection = mysql.connector.connect(user = "root", password = "Password", database = "UserDetails")
    query = ("insert into UserDetails (username, password) values (%s, %s)")
    cursor = connection.cursor()
    cursor.execute(query,(username, password))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

def getArticles():
    returnHTML = ""
    connection = mysql.connector.connect(user = "root", password = "Password", database = "UserDetails")
    query = ("select title from articles")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)

    for a in cursor:
        returnHTML += str(a['title'])+"<br>"

    if len(returnHTML) == 0:
        returnHTML = "There are no articles"
    
    return returnHTML

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
    <p>
        <a href="Articles.html">
            <!--States the page the thumbnail will link to-->
            <img height=200 width=300 src="a e s t h e t i c.jpg" />
            <!--Sets the height and width of the thumbnail image, and the image to be displayed-->
        <a/> 
        <a href="User Reviews.html">
            <!--States the page the thumbnail will link to-->
            <img height=200 width=300 src="For Honor.jpg" />
            <!--Sets the height and width of the thumbnail image, and the image to be displayed-->
        <a/>
    </p> </body> </html>''' %(loginHTML)
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

@app.route("/UserReviews")
def userReviews():
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
    </p> </body> </html>'''
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
