#Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175

from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector


app = Flask(__name__, static_url_path='')

#connect to database
conn = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    database='zipcodes',
    buffered = True
)
cursor = conn.cursor()

# search for zip from zipcodes database
@app.route('/search_zip/<zip>')
def search_zip(zip):
    # Get data from database
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip = %s", [zip])
    test = cursor.rowcount
    if test != 1:
        return zip + " was not found"
    else:
        searched = cursor.fetchall()
        return 'Success! Here you go: %s' % searched

# update population for a specified zip from zipcodes database
@app.route('/update_zip_pop/<zip> <update_pop>')
def update_zip_pop(zip, update_pop):
    cursor.execute("SELECT * FROM zipcodes WHERE zip = %s", [zip])
    test = cursor.rowcount
    if test != 1:
        return zip + " was not found"
    else:
        cursor.execute("UPDATE zipcodes SET Population = %s WHERE zip = %s;", [update_pop, zip])
        cursor.execute("SELECT * FROM zipcodes WHERE zip = %s and Population = %s", [zip, update_pop])
        test1 = cursor.rowcount
        if test1 != 1:
            return zip + "  failed to update"
        else:
            return 'Population has been updated successfully for Zip: %s' % zip

# update webpage
@app.route('/update',methods = ['POST'])
def update():
       r = request.form['u_zip']
       r2 = request.form['u_pop']
       return redirect(url_for('update_zip_pop', zip = r, update_pop = r2))

# search page
@app.route('/search', methods=['GET'])
def search():
       r = request.args.get('s_zip')
       return redirect(url_for('search_zip', zip = r))

# root of web server and gots to template (index.html)
@app.route('/')
def root():
   return render_template('index.html')


#main
if __name__ == '__main__':
   app.run(debug = True)