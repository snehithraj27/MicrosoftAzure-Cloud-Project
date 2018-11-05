# Author: Snehith Raj Bada
 
import io,os
from flask import Flask,render_template,request
import csv
import sqlite3
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

#Create Database
conn = sqlite3.connect('database.db')
try:
    conn.execute('CREATE TABLE if not exists people(Name varchar,Grade varchar,Room varchar,TelNum varchar,Picture blob,Keywords varchar)')
    print('Table created successfully')
except:
    print("Table not created")
finally:
    conn.close()

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Insert data into the table
@app.route('/insertdata', methods=['POST'])
def insert_data():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    next(csv_input)
    print(csv_input)
    for row in csv_input:
        print(row)
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO people(Name,Grade,Room,TelNum,Picture,Keywords) VALUES (?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5]))
                print(1)
                con.commit()
                msg = "Record successfully added"
                print (msg)
            msg="Records inserted successfully"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con.close()
    return render_template('result.html',msg=msg)

# Display all records
@app.route('/getrecords', methods=['POST'])
def get_records():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from people")
    con.commit()
    rows = cur.fetchall();
    print(rows)
    con.close()
    return render_template("data.html", msg=rows)

# Delete all records
@app.route('/deleterecords', methods=['POST'])
def delete_records():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("delete from people")
    con.commit()
    rows = cur.fetchall();
    print(rows)
    con.close()
    return render_template("result.html", msg="All records deleted")

# Upload and store images
@app.route('/uploadimage', methods=['POST'])
def upload_image():
    print(1)
    if 'image' in request.files:
        filename = photos.save(request.files['image'])
        return filename
    return render_template('home.html',msg="Image successfully uploaded. Upload another image")

# Search for name and display picture
@app.route('/searchname', methods=['POST'])
def search_name():
    name=request.form['name']
    print(name)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select Picture from people where Name=?",(name,))
    con.commit()
    rows = list(cur.fetchall());
    print(rows[0][0])
    con.close()
    filename = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], rows[0][0])
    print(filename)
    return render_template("image.html", image=filename,msg=name)

# Search pictures based on grade
@app.route('/searchpicture', methods=['POST'])
def search_picture():
    grade=request.form['grade']
    print(grade)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select Name,Picture from people where Grade<?",(grade,))
    con.commit()
    rows = list(cur.fetchall());
    print(rows)
    con.close()
    result=[]
    for row in rows:
        res=[]
        res.append(row[0])
        res.append(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], row[1]))
        result.append(res)
    print(result)
    return render_template("images.html", images=result)

# Add picture for name
@app.route('/addpicture', methods=['POST'])
def add_picture():
    name = request.form['name']
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    keyword=name.lower()+'.jpg'
    cur.execute("UPDATE people SET Picture = ? WHERE Name =?", (keyword, name,))
    con.commit()
    con.close()
    if 'image' in request.files:
        filename = photos.save(request.files['image'])
        return filename
    return render_template('home.html',msg="Image successfully uploaded. Upload another image")

# Remove name from the database
@app.route('/removename', methods=['POST'])
def remove_name():
    name=request.form['remove_name']
    print(name)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("delete from people where Name=?",(name,))
    con.commit()
    con.close()
    return render_template("result.html", msg="Successfully deleted")

# Change keyword for given name
@app.route('/changekeyword', methods=['POST'])
def change_keyword():
    name=request.form['name']
    keyword=request.form['keyword']
    print(name,keyword)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("UPDATE people SET Keywords = ? WHERE Name =?",(keyword,name,))
    con.commit()
    con.close()
    return render_template("result.html", msg="Successfully updated")

# Change grade for given name
@app.route('/changegrade', methods=['POST'])
def change_grade():
    name = request.form['name']
    grade = request.form['grade']
    print(name)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("UPDATE people SET Grade = ? WHERE Name =?", (grade, name,))
    con.commit()
    con.close()
    return render_template("result.html", msg="Successfully updated")

if __name__ == '__main__':
    app.run(debug=True)