from flask import Flask, render_template         
import pymysql

app = Flask(__name__, template_folder='templates')               
 
@app.route('/<yourname>')                     
def index(yourname):

    #connecting to a MySQLdb
    db=pymysql.connect(user='Nypuser', passwd='password', host='localhost', db='Part2Data')
    cursor = db.cursor()
    
    cursor.execute("Select * from Part2Data.Part2Data")
    results = cursor.fetchall()

    db.close()

    message = yourname + "'s Project Part 2 Data"  
    return render_template('sql-data.html', message=message, results=results)
 
if __name__ == '__main__':
    app.run()
