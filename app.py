from flask import Flask,render_template,request,redirect
from flask_moment import Moment
import pymongo
import datetime
app=Flask(__name__)
file=open('connectionstring.txt','r')
connectionstring=file.read().strip()
file.close()
app.config["MONGO_URI"]=pymongo.MongoClient(connectionstring)
database=app.config["MONGO_URI"]["Note_Manager"]
collection=database["Notes"]

moment=Moment(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addnote',methods=['GET','POST'])
def addnote():
    if request.method=='GET':
        return render_template('addnote.html')
    else:
        information=request.form
        person_name=information['person_name']
        person_note=information['person_note']
        time_of_posting=datetime.datetime.utcnow()
        note={'name':person_name,'note':person_note,'time':time_of_posting}
        collection.insert_one(note)
        return redirect('/addnote')

@app.route('/shownote')
def shownote():
    data=collection.find()
    notes=[]
    for i in data:
        notes.append(i)
    notes.reverse()
    return render_template('shownote.html',notes=notes)









if __name__=="__main__":
    app.run()