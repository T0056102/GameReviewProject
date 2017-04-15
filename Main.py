from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
import pypyodbc

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
      body {
        background-image: url("firewatch-wallpaper-12.jpg");
        background-repeat: no-repeat;
    }
    ul { list-style-type: none; padding: 0; margin: 0; background-color: #8E44AD; } li { display: inline-block; } li a { display: block; padding: 10px; color: #FDFEFE; } li a:hover { background-color: #BB8FCE; } </style> 
    <!--Formats the main bar at the top of the screen--> 
    </style>
    </head>'''
    return header

def headBar(pageTitle):
    headText = '''<body>
    <h1>%s</h1>
    <!--Sets the title of the page-->
    <nav> <ul>''' % (pageTitle)
    return headText
    
@app.route("/")
def main():
    global linkList
    pageContent = commonHeader()
    pageContent += headBar("Fenrir")
    for taskBar in linkList:
        pageContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
    pageContent+= '''</ul> </nav>
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
    </p> </body> </html>'''
    return pageContent

@app.route("/Articles")
def articles():
    global linkList
    pageContent = commonHeader()
    pageContent += headBar("Articles")
    for taskBar in linkList:
        pageContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
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

@app.route("/UserReviews")
def userReviews():
    pageContent = commonHeader()
    pageContent += headBar("User Reviews")
    for taskBar in linkList:
        pageContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
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
    for taskBar in linkList:
        pageContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
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
    for taskBar in linkList:
        pageContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
    pageContent +='''</ul> </nav>''' 
    return pageContent

@app.route("/Login", methods=['GET', 'POST'])
def login():
    print "request.method = %s" % (request.method)
    if request.method == 'POST':
        print "Re-directing"
        return redirect(url_for("main"))
    print "Display login"
    pageContent = commonHeader()
    pageContent += headBar("Articles")
    for taskBar in linkList:
        pageContent += '<li><a href="%s">%s</a></li>' % (taskBar[0],taskBar[1])
    pageContent +='''</ul> </nav> <p>
    </p>
    <form action="/Login" method = POST>
    <!--Creates the form for the login boxes-->
      <div class="container">
      <!--Creates a container to put the login boxes in-->
        <label><b>Username</b></label>
        <!--Labels the username box-->
        <input type="text" 
        placeholder="Enter Username" 
        name="uname" 
        required>
        <!--[input type="text"] Sets the data type to text
        [placeholder="Enter Username"] sets the placeholder text to be "Enter Username" 
        [name="uname"] names the box "username"
        [required] makes the data required-->

        <label><b>Password</b></label>
        <!--Labels the password box-->
        <input type="password" 
        placeholder="Enter Password" 
        name="psw" 
        required>
        <!--[input type="password"] Sets the data type to password so it will be hidden
        [placeholder="Enter Password"] sets the placeholder text to be "Enter Password"
        [name="psw"] names the box "psw"
        [required] makes the data requires-->

        <button type="submit">Login</button>
        <!--Creates the login button-->
      </div>
    <p>
    </p>
      <div class="container" style="background-color:#">
        <span class="psw">Don't have an account? <a href="#">Create one here</a></span>
        <!--Creates a link to the create account page for if a user does not yet have an account-->
      </div>
    </form> </body> </html>''' 
    return pageContent

if __name__ == "__main__":
    app.run()
