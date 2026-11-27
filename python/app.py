# Smart Window Energy Guard - Flask dashboard
#
# Shows the readings logged by sensor_processor.py, newest first, refreshing
# every 5 seconds. Open http://<pi-address>:5000/ or http://<pi-address>:5000/<yourname>
# Database settings can be overridden with the same environment variables as
# sensor_processor.py (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME).

import os

from flask import Flask, render_template
import pymysql

app = Flask(__name__)   # templates/ sits next to this file

DB_SETTINGS = {
    "user": os.environ.get("DB_USER", "Nypuser"),
    "passwd": os.environ.get("DB_PASSWORD", "password"),
    "host": os.environ.get("DB_HOST", "localhost"),
    "db": os.environ.get("DB_NAME", "Part2Data"),
}


@app.route('/')
@app.route('/<yourname>')
def index(yourname=None):

    #connecting to a MySQLdb
    db = pymysql.connect(**DB_SETTINGS)
    try:
        cursor = db.cursor()
        # newest readings first (column 1 is the auto-increment row number)
        cursor.execute("Select * from Part2Data ORDER BY 1 DESC LIMIT 200")
        results = cursor.fetchall()
    finally:
        db.close()

    message = (yourname + "'s " if yourname else "") + "Project Part 2 Data"
    return render_template('sql-data.html', message=message, results=results)


if __name__ == '__main__':
    # FLASK_HOST=0.0.0.0 lets other devices on the network open the dashboard
    app.run(host=os.environ.get("FLASK_HOST", "127.0.0.1"), port=5000)
