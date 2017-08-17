#Imports functions needed
from flask import Flask, request, url_for, redirect, make_response
from random import randint
from subprocess import call
from email.mime.text import MIMEText
import sys
import mysql.connector
import smtplib
import base64
from email import message

app = Flask(__name__)

#Start-up function
@app.before_first_request
def createDatabase():
    try:
        #Trie to connect to the database
        connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    except:
        #If it can't then it tries to create a new database in its place 
        try:
            connection = mysql.connector.connect(user = "root", password = "Password1!")
            query = ("create database GameReview;")
            cursor = connection.cursor()
            cursor.execute(query)
            query = ("use GameReview;")
            cursor = connection.cursor()
            cursor.execute(query)
            #Creates the user details table which contains columns for username, password and coockie, which are all strings of up to 32 characters, and email which is a string of up to 256 characters
            query = ("create table UserDetails (username varchar(32), password varchar(32), cookie varchar(32), email varchar(256));")
            cursor = connection.cursor()
            cursor.execute(query)
            #Creates the articles table which contains columns for ArticleID, which is the primary key and is increased by 1 for each record added, title, img_url, and video_url, which are all strings of up to 256 characters
            #Body, which is an unlimited string, score which is a number and genre and rating which are both integers 
            query = ("create table articles (ArticleID mediumint not null auto_increment, title varchar(256), img_url varchar(256), video_url varchar(256), body text, score decimal(3,1), genre decimal(2,0), rating decimal(2,0), PRIMARY KEY (ArticleID));")
            cursor = connection.cursor()
            cursor.execute(query)
            #Creates the user articles table which contains columns for ArticleID, which is the primary key and is increased by 1 for each record added, title, img_url, and video_url, which are all strings of up to 256 characters
            #Body, which is an unlimited string, score which is a number and genre and rating which are both integers 
            query = ("create table UserArticles (ArticleID mediumint not null auto_increment, title varchar(256), img_url varchar(256), video_url varchar(256), body text, score decimal(3,1), genre decimal(2,0), rating decimal(2,0), PRIMARY KEY (ArticleID));")
            cursor = connection.cursor()
            cursor.execute(query)
            #Creates the upcoming releases table which contains the columns: title and platforms, which are both strings of up to 256 characters, as well as the date which is a string of up to 8 characters
            query = ("create table UpcomingReleases (title varchar(256), platforms varchar(256), date varchar(8));")
            cursor = connection.cursor()
            cursor.execute(query)
            #Commits the tables to the database
            query = ("commit;")
            cursor = connection.cursor()
            cursor.execute(query)
        #If it can't do that then it ends the code
        except Exception, e:
            print(e)
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
    cursor.execute(query,(username, decryptXOR(str(password))))
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

#Defines the function that will log the user out
def logUserOut(secretNumber):
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ('update UserDetails set cookie = "" where cookie = "%s"' % (secretNumber))
    cursor = connection.cursor()
    cursor.execute(query)
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)
#Defines the function that will check if entered details for creating the account are already in the database
def loginExists(username):
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ('select username from UserDetails where username = "%s"' % (username))
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.fetchall()
    if cursor.rowcount > 0:
        return True
    return False

#Defines the function that will store new accounts on the database
def storeAccount(username, password, email):
    #connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("insert into UserDetails (username, password, email) values (%s, %s, %s)")
    cursor = connection.cursor()
    #Commits the new information to the database, encrypting the password in the process
    cursor.execute(query,(username, encryptXOR(str(password)), email))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

#Defines the quick dort function
def quickSort(data,orderBy):
    #Creates the list of numbers greater than the pivot
    higherList = []
    #Creates the list of numbers lower than the pivot
    lowerList = []
    #Finds the midpoint of the list
    midpoint = len(data)/2
    a = 0
    while a < len(data):
        if a == midpoint:
            pass
        elif (orderBy=="0" and data[a][0] < data[midpoint][0]) or (orderBy=="1" and data[a][0] > data[midpoint][0]):
            lowerList.append(data[a])
        else:
            higherList.append(data[a])
        a += 1
    if len(lowerList) > 1:
        lowerList = quickSort(lowerList,orderBy)
    if len(higherList) > 1:
        higherList = quickSort(higherList,orderBy)
    lowerList.append(data[midpoint])
    return lowerList + higherList

#Defines the function that will fetch the articles from the database
def getArticles(genre, orderBy):
    returnHTML = ""
    #connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    whereStatement = ""
    #If the user has filtered to a specific genre then only articles with that genre value are displayed
    if genre != None and genre != 0:
        whereStatement = "where genre = %s" % (genre)
    query = ("select ArticleID, title, img_url, video_url from articles %s" % (whereStatement))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    #If the user hasn't chosen to sort the articles, they are sorted from oldest to newest by default
    if orderBy == None:
        orderBy = "0"
    sortList = []
    for a in cursor:
        sortList.append([a['ArticleID'], "<div class='article_box'><a href='/Articles/%s'><img class='article_img' src='%s'><br>%s</a></div>" % (str(a['ArticleID']), str(a['img_url']), str(a['video_url']),str(a['title']))])
    if len(sortList)==0:
        return "There are no articles"   
    for a in quickSort(sortList,orderBy):
        returnHTML += a[1]
    return returnHTML

#Defines the function that will fetch the user articles from the database
def getUserArticles(genre, orderBy):
    returnHTML = ""
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    whereStatement = ""
    #If the user has filtered to a specific genre then only articles with that genre value are displayed
    if genre != None and genre != 0:
        whereStatement = "where genre = %s" % (genre)
    query = ("select ArticleID, title, img_url, video_url from UserArticles %s" % (whereStatement))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    #If the user hasn't chosen to sort the articles, they are sorted from oldest to newest by default
    if orderBy == None:
        orderBy = "0"
    sortList = []
    for a in cursor:
        sortList.append([a['ArticleID'], "<div class='article_box'><a href='/UserReviews/%s'><img class='article_img' src='%s'><br>%s</a></div>" % (str(a['ArticleID']), str(a['img_url']),str(a['title']))])
    if len(sortList)==0:
        return "There are no articles"   
    for a in quickSort(sortList,orderBy):
        returnHTML += a[1]  
    return returnHTML

#Defines the function that will fetch the details of the articles from the database
def getArticleDetails(ArticleID):
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select ArticleID, title, img_url, video_url, body, score from articles where ArticleID = '%s'" % (ArticleID))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    #Uses a acursor to fetch the data and place it in this format
    for a in cursor:
        return "<h1>%s</h1><p>%s</p><img src='%s'><p>%s</p><p>%s</p>" % (str(a['title']), str(a['rating']), str(a['img_url']), str(a['video_url']), str(a['body']), str(a['score']))

#Defines the function that will fetch the details of the user articles from the database
def getUserArticleDetails(ArticleID):
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select ArticleID, title, rating, img_url, video_url, body, score from UserArticles where ArticleID = '%s'" % (ArticleID))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    #Uses a acursor to fetch the data and place it in this format
    for a in cursor:
        return "<h1>%s</h1><p>%s</p><img src='%s'><p><iframe width='420' height='315' src='%s'></iframe></p><p>%s</p><p>%s</p>" % (str(a['title']), str(a['rating']), str(a['img_url']), str(a['video_url']), str(a['body']), str(a['score']))

#Defines the function that will validate the details entered by a user when they are creating an article
def checkCreate(title, score, body, image, video):
    #If there isn't a title the user is told that they need to enter something into the title box
    if title == "":
        return "you must enter a title"
    #If the title is more than 256 characters in length then they are told that the title can't be more than 256 characters long
    if len(title)>256:
        return "title too long, cannot be more than 256 characters long"
    #If the user hasn't entered a score they are told that they must enter a score
    if score == "":
        return "you must enter a score"
    #If the score is not a number then it is rejected and the user is told that it must be a number
    try:
        float(score)
    except:
        return "score must be a number"
    #If the score is greater than 10 or less than 0 they are told that it must be within that range
    if float(score) >10 or float(score)<0:
        return "score (%s) must be between 0 and 10" % (score)
    #If the body is empty the user is told that they must enter a body
    if body == "":
        return "you must enter a body"
    #If the image url box is empty the user is told that they must enter an image url
    if image == "":
        return "you must enter an image URL"
    #If the image url is longer than 256 characters it is considered false and the user is told the range that it must be in
    if len(image) >256:
        return "Image URL must beat most 256 characters long"
    #If the image url box is empty the user is told that they must enter an video url
    if video == "":
        return "You must enter a video URL"
    if len(video) >256:
        return "Video URL must be at most 256 characters long"
    return ""

#Defines the function that will create new reviews
def createReview(title, score, body, image, video, genre):
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("insert into UserArticles (title, img_url, video_url, body, score, genre, rating) values (%s, %s, %s, %s, %s, %s, '0')")
    cursor = connection.cursor()
    #Inputs the new title, image, video, body, score and genre
    cursor.execute(query,(title, image, video, body, score, genre))
    query = ("commit")
    cursor = connection.cursor()
    cursor.execute(query)

#Defines the function that will fetch the list of upcoming releases from the database
def getUpcoming():
    returnHTML = "<table><tr><td>Date</td><td>Title</td><td>Platforms</td></tr>"
    upcomingFound = False
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    query = ("select title, platforms, date from UpcomingReleases")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    #Fetches the records from the database
    for a in cursor:
        upcomingFound = True
        returnHTML += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a['date'], a['title'], a['platforms'])
    #If there aren't any records the message "There are no upcoming releases" is displayed
    if upcomingFound == False:
        returnHTML = "There are no upcoming releases"
    return returnHTML

#Defines the function that will create the genre drop down box
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

#Defines the function that will create the sorting drop down box
def sortBy(currentSort):
    submitText = 'onchange="this.form.submit()"'
    selectedItem=['','']
    if currentSort==None or currentSort=="0":
        selectedItem[0]=" selected"
    else:
        selectedItem[1]=" selected"
    return '''<label>Sort By</label>
                <!--Labels the drop down box-->
                <select name="orderBy" id = "orderBy" %s>
                <!--Creates the list of things to display in the drop down box-->
                    <option value = "0"%s>Oldest to Newest</option>
                    <option value = "1"%s>Newest to Oldest</option>
                </select>''' % (submitText,selectedItem[0],selectedItem[1])

#Defines the ecryption function
def encryptXOR(s, key="\x101Z"):
    output = ""
    for character in s:
        #Individually changes the ascii values of each of the letters in the password
        for letter in key:
            character = chr(ord(character) ^ ord(letter))
        output += character
    return output

#Defines the decryption function
def decryptXOR(s, key="\x101Z"):
    output = ""
    for character in s:
        #Does the opposite of the encryption function in order to return the password to it's original form
        for letter in key[::-1]:
            character = chr(ord(character) ^ ord(letter))
        output += character
    return output

#Defines the function that will send an email to the administrator
def sendEmail(mail_message):
#    msg = MIMEText(message)
#    msg['Subject'] = "subject"
#    msg['From'] = "t0056102@cardinalnewman.ac.uk"
#    msg['To'] = "fenrir.reviews@gmail.com"

    msg = message.Message()
    msg.add_header('from','t0056102@cardinalnewman.ac.uk')
    msg.add_header('to','fenrir.reviews@gmail.com')
    msg.add_header('subject', 't0056102@cardinalnewman.ac.uk')
    msg.set_payload(mail_message)
    
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login("fenrir.reviews@gmail.com", base64.b64decode('UGE1NXdvcmQxIQ=='))
    s.sendmail("t0056102@cardinalnewman.ac.uk", ["fenrir.reviews@gmail.com"], msg.as_string())
    s.quit()
    return 

#Sets this paige to  be the default  
@app.route("/")
#Creates the main page of the website
def main():
    #Displays the bar of page links defined earlier
    global linkList
    #Connects to the database
    connection = mysql.connector.connect(user = "root", password = "Password1!", database = "GameReview")
    loginHTML = ""
    #Checks if the user's cookie exists
    if 'secretNum' in request.cookies:
        secretNum = request.cookies.get('secretNum')
        #If it does then "user logged in" is displayed at the top of the page
        if getUserBySecret(secretNum) == True:
            loginHTML = "user logged in"
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Fenrir"
    pageContent += headBar("Fenrir")
    #inputs the HTML of the page into the website
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

#Sets the page to display when /Articles/(the article id) is at the end of the URL
@app.route("/Articles/<articleID>")
#Creates the page of the articles
def articleDetails(articleID):
    #Displays the bar of page links defined earlier
    global linkList
    articleDetails = getArticleDetails(articleID)
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Articles"
    pageContent += headBar("Articles")
    #Inputs the article details from the database where it says %s
    pageContent +='''</ul> </nav> <p>%s</p>''' % (articleDetails)
    return pageContent

#Sets the page to display when /Articles is at the end of the URL
@app.route("/Articles", methods = ['GET', 'POST'])
#Creates the page where the list of articles is displayed
def articles():
    #Displays the bar of page links defined earlier
    global linkList
    #If the user has selected a specific genre or way for the articles to be ordered, they are displayed as such
    listArticles = getArticles(request.form.get('genre'), request.form.get('orderBy'))
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Articles"
    pageContent += headBar("Articles")
    #Formats the page and gets the needed data from the database and implements it where the %s' are located
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
    </body> </html>''' % (genreList(True), sortBy(request.form.get('orderBy')), listArticles)
    return pageContent

#Sets the page to display when /CreateUserReview is at the end of the URL
@app.route("/CreateUserReview", methods = ['GET', 'POST'])
#Creates the page where users can create their own reviews
def createUserReviews():
    #Displays the bar of page links defined earlier
    global linkList
    errorMessage = ""
    #Checks if the form has been completed and, if it has, redirects to the user reviews page
    if request.method == 'POST':
        errorMessage = checkCreate(request.form['title'], request.form['score'], request.form['body'], request.form['image'], request.form['video'])
        if errorMessage == "":
            createReview(request.form['title'], request.form['score'], request.form['body'], request.form['image'], request.form['video'], request.form['genre'])
            return redirect(url_for('userReviews'))
    listUserArticles = getUserArticles(request.form.get('genre'), request.form.get('orderBy'))
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Create a Review"
    pageContent += headBar("Create a Review")
    #Creates the form which users have to fill in to create a review
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
            <label><b>Video</b></label>
            <!--Labels the video box-->
            <input type="text" 
            placeholder="Enter Video URL" 
            name="video" 
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

#Sets the page to display when /UserReviews is at the end of the URL
@app.route("/UserReviews", methods = ['GET', 'POST'])
#Creates the page where the list of user articles will be displayed
def userReviews():
    #Displays the bar of page links defined earlier
    global linkList
    #If the user has selected a specific genre or way for the articles to be ordered, they are displayed as such
    listUserArticles = getUserArticles(request.form.get('genre'), request.form.get('orderBy'))
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "User Reviews"
    pageContent += headBar("User Reviews")
    displayButton = ""
    #Only displays the button that takes the user to the review creation form if they are logged in
    if 'secretNum' in request.cookies:
        secretNum = request.cookies.get('secretNum')
        if getUserBySecret(secretNum) == True:
            displayButton = '''<form action="/CreateUserReview" method = GET>
                            <button type="submit">Create article</button>'''
    #Formats the page and gets the needed data from the database and implements it where the %s' are located 
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
    %s
    </form>
    </p>
    %s
    </body> </html>''' % (genreList(True), sortBy(request.form.get('orderBy')), displayButton, listUserArticles)
    return pageContent

#Sets the page to display when /UserReviews/(the article's ID) is at the end of the URL
@app.route("/UserReviews/<articleID>")
#Creates the user reviews pages
def UserArticleDetails(articleID):
    #Displays the bar of page links defined earlier
    global linkList
    #Fetches the article's details from the database
    articleDetails = getUserArticleDetails(articleID)
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "User Reviews"
    pageContent += headBar("User Reviews")
    #Inputs the article details from the database where it says %s
    pageContent +='''</ul> </nav> <p>%s</p>''' % (articleDetails)
    return pageContent

#Sets the page to display when /UpcomingReleases is at the end of the URL
@app.route("/UpcomingReleases")
#Creates the page where the list of upcoming releases is displayed
def upcomingReleases():
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Upcoming reviews"
    pageContent += headBar("Upcoming Releases")
    #Inputs the list from the database where it says %s
    pageContent +='''</ul> </nav> <p>
    %s
    </p> </body> </html>''' % (getUpcoming())
    return pageContent

#Sets the page to display when /Contact is at the end of the URL
@app.route("/Contact", methods=['GET', 'POST'])
#Creates the page where users can send the Admin an email
def contact():
    #Sends the email and redirects to the main page
    if request.method == 'POST':
        sendEmail(request.form['message'])
        return(redirect(url_for("main")))
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Contact"
    pageContent += headBar("Contact")
    #Formats the contact form
    pageContent +='''</ul> </nav>
    <form action="/Contact" method = POST>
    <div class="container">
        <label><b>Enter your message here</b></label>
        <input type="text"
        placeholder="Enter message" 
        name="message" 
        required>
        <button type="submit">Send</button>
        <!--Creates the button that will send the email-->
    </div>
    </form>
    </body> </html>''' 
    return pageContent

#Sets the page to display when /Login is at the end of the URL
@app.route("/Login", methods=['GET', 'POST'])
#Creates the login page
def login():
    falseLogin = ""
    #If the inputted detailes are not in the database the user is not logged in and are given a message telling them that their login was wincorrect
    if request.method == 'POST':
        #If the details were correct a cookie is created for the user, the user is redirected to the main page, and the login link at the top of the page is replaced with a logout button
        if checkLogin(request.form['username'], request.form['password']):
            cookieNum = secretNumber()
            response = make_response(redirect(url_for("main")))
            response.set_cookie('secretNum', cookieNum)
            updateUserCookie(request.form["username"], cookieNum)
            linkList[5][1] = "Logout"
            return response
        falseLogin = "Your login details were incorrect"
    if 'secretNum' in request.cookies:
        secretNum = request.cookies.get('secretNum')
        if getUserBySecret(secretNum) == True:
            logUserOut (secretNum)
            linkList[5][1] = "Login"
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Login"
    pageContent += headBar("Login")
    #Formats the login form
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

#Sets the page to display when /CreateAccount is at the end of the URL
@app.route("/CreateAccount", methods=['GET', 'POST'])
#Created the page for creating an account
def createAccount():
    falseCreate = ""
    #If the username is already in the database the user is not allowed to use it
    if request.method == 'POST':
        if loginExists(request.form['username']):
            falseCreate = "username is already taken"
        #If the password is not the same in both boxes the user is informed, this is to prevent typos in the passwords
        else:
            if request.form['password1'] != request.form['password2']:
                falseCreate = "passwords do not match"
            #Sores the new record in the database and redirects to the login page
            else:
                storeAccount(request.form['username'], request.form['password1'], request.form['email'])
                return(redirect(url_for("login")))
    pageContent = commonHeader()
    #Sets the title at the top of the page to be "Create Account"
    pageContent += headBar("Create Account")
    #Formats the create account page
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

        <label><b>E-Mail</b></label>
        <!--Labels the email box-->
        <input type="text" 
        placeholder="Enter E-Mail" 
        name="email" 
        required>
        <!--[input type="text"] Sets the data type to be text
        [placeholder="Enter E-Mail"] sets the placeholder text to be "Enter E-Mail"
        [name="email"] names the box "email"
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
    run_port=5000
    if len(sys.argv) > 1:
      run_port=sys.argv[1]
    app.run(port=run_port)
