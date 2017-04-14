from flask import Flask
app = Flask(__name__)

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
</head>
'''
    return header
    
@app.route("/")
def main():
    linkList = [["/","Home"],
                ["Articles","Articles"],
                ["UserReviews","User Reviews"],
                ["UpcomingReleases","Upcoming Releases"],
                ["Contact","Contact"],
                ["Login","Login"]
               ]
    pageContent = commonHeader()
    pageContent += '''<body>
    <h1>Fenrir</h1>
    <!--Sets the title of the page-->
    <nav> <ul>'''
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
    </p>
    </body>
    </html>'''
    return pageContent

@app.route("/Articles")
def articles():
    pageContent = commonHeader()
    pageContent +='''<body>articles</body></html>'''
    return pageContent

if __name__ == "__main__":
    app.run()
