### This is the default ckselu_pythonanywhere_com_wsgi.py file
## used on pythonanywhere.com to show a class example (including DB).

import mysql.connector
# import a Query String parser
from urllib.parse import parse_qs
outp=""

my_form1 = """<html>
<body><h1>Welcome to Test</h1><form action="./form2" method="GET">
<p>First name: <input type="text" name="first_name" value={}>
<p>Last name: <input type="text" name="last_name" value={}>
<p><input type="submit" name="Submit"></form></body>
</html>"""

#The following works with my_form1_1.format(XX=myfirst, YY=mylast)
my_form1_1 = """<html>
<body><h1>Welcome to Test</h1><form action="./form2" method="GET">
<p>First name: <input type="text" name="first_name" value={XX}>
<p>Last name: <input type="text" name="last_name" value={YY}>
<p><input type="submit" name="Submit"></form></body>
</html>"""

def show_form1():
    global my_form1
    myfirst='Cris'
    mylast='Kouts'
    newstr=my_form1.format(myfirst, mylast)
 ##   newstr=my_form1_1.format(XX=myfirst, YY=mylast) #this works with my_form1_1
    return newstr

def show_form2():
    global myQueryString
    ## We can put processing here like this:
    myFirstName = myQueryString['first_name'][0]
    myLastName  = myQueryString['last_name'][0]
    myresponse = 'Hello there {} {}.'.format(str(myFirstName), str(myLastName))
    myresponse += my_form1.format('NewFirst', 'NewLast')
    return myresponse

def dbDemo():
    global outp
    outp=""
    ## Define variables needed throughout the script
    DBuser="ckselu"
    DBpass="cksclass"
    DB="ckselu$Bookstore"
    DBtable="Books"
    DBhost ="ckselu.mysql.pythonanywhere-services.com"

    ## Now open the DB
    mydb = mysql.connector.connect(host=DBhost, user=DBuser, passwd=XXXXXXX, database=DB)
    outp += "<p>DB Connected...<br>"

    ##-- and create database object
    mycursor = mydb.cursor()

    ## Database is now ready for use

    ## Define a query for the DB, possibly using form inputs from a user
    query = "SELECT * FROM " + "  " + DBtable

    outp += "<p>Query is " + query + "<p>\n"

    ## Execute the query
    mycursor.execute(query)

    ####### Handle Results:
    results = mycursor.fetchall()      ## Now all items retrieved from DB are in "results"
    ## Print all the results
    for row in results:
        outp += ', '.join(map(str,row))  ## join all elements of "row" mapped as strings separated by ", "
        outp += "<br>\n" ## Insert an HTML line break after each element

    mydb.close()     ## Finished; Close the DB
    outp += "<p>I am done<p>"


### The following is the router ###

def application(environ, start_response):
    global outp

    mycookie = environ.get("HTTP_COOKIE", "")
    if environ.get('PATH_INFO') == '/':
        status = '200 OK'
        content = "HELLO_WORLD"
        ## start_response.set_cookie('userID', user)
    elif environ.get('PATH_INFO') == '/showcookie' :
        status = '200 OK'
        content = 'Cookie is ' + mycookie + '<p>'
    elif environ.get('PATH_INFO') == '/runDB' :
        dbDemo()
        status = '200 OK'
        content = outp
    elif environ.get('PATH_INFO') == '/form1' :
 ##       content = str(show_form1())
        content = show_form1()
        status = '200 OK'
    elif environ.get('PATH_INFO') == '/form2' :
        global myQueryString
        myQueryString = parse_qs(environ.get('QUERY_STRING'))
 ##       content = str(show_form2())
        content = show_form2()
        status = '200 OK'
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'

## without cookies
#    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
## using cookies
    response_headers = [('Content-Type', 'text/html'), ('Set-Cookie', 'name=Agagou; Expires=120; Max-Age=360; Path=/'), ('Set-Cookie', 'lala=Atsatsou; Expires=120; Max-Age=360; Path=/'), ('Content-Length', str(len(content)))]
    start_response(status, response_headers)
    yield content.encode('utf8')
