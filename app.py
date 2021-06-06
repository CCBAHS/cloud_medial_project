# Flask backend 
from flask import Flask, render_template, request,redirect
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from ext_classes import codes
from ext_classes import mailingbot

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/test"

mongo = PyMongo(app)

@app.errorhandler(404)
def page_not_found(e):
    return " Sorry But a Bad Request "


@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET','POST'])
def login():
    '''
        Recieves login credentials from the frontend and sends it to the user function to create session for the user.
    '''
    if request.method == 'POST':
        username = request.form['userid']
        password = request.form['password']
        userid = mongo.db.test_collection.find_one_or_404({"username":username,"password":password})
        print(userid)
        return redirect(f"/user/{userid['username']}")
    else:
        return render_template('patient-login-page.html')

@app.route('/user/<username>')
def user(username):
    '''
        Creates session for a specific user.
    '''
    userid = mongo.db.test_collection.find_one_or_404({"username":username})
    return mongo.send_file(userid['profile_photo'])


@app.route('/account', methods=['GET','POST'])
def account():
    '''
        Recieves data from the frontend and stores it to the mongodb database.
    ''' 
    if request.method == 'POST':
        code = codes()
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        title = request.form['identity']
        # needed to be changed
        password = request.form['password-create']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        pin = request.form['pincode']
        mobile = request.form['mobileno']
        email = request.form['emailid']
        adhaar = request.form['adhaar']
        time_created = datetime.now()        
        username = title[:3].upper() + code.statecode(state) + dob.split('-')[0][-2:] + str(code.usernumber(title,state))
        filename = username + '.png'
        print(filename)
        try:
            if not mongo.db.test_collection.find_one({'adhaar':adhaar}):
                mongo.save_file(filename,request.files['photo'])
                print(' Profile Image Saved Successfully')
                mongo.db.test_collection.insert_one({"name":name,
                                                    "dob":dob,
                                                    "gender":gender,
                                                    "title":title,
                                                    "username":username,
                                                    "password":password,
                                                    "address":address,
                                                    "state":state,
                                                    "city":city,
                                                    "pin":pin,
                                                    "mobile":mobile,
                                                    "email":email,
                                                    "adhaar":adhaar,
                                                    "profile_photo":filename,
                                                    "time_created":time_created})
                print(' Data Object Inserted Successfully ')
                mailbot = mailingbot()
                mailbot.send_message(email,{'name':name,'username':username})
            else:
                page_not_found(Exception)
        except Exception:
            print(Exception)
            params ={'title':'Reset Password','verify':True}
        return render_template('middle_page.html',params=params)
    else:
        return 'Hello World'

@app.route('/reset', methods=['GET','POST'])
def reset():
    '''
        Recieves Email Address of the user checks for the validity and sends mail for resetting the password.
    '''
    if request.method == 'POST':
        username = request.form['reset-userid']
        adhaar = request.form['reset-adhaar']
        user = mongo.db.test_collection.find_one({'username': username,'adhaar':adhaar})
        if user:
            email = user['email']
            name = user['name']
            mailbot = mailingbot()
            otp = mailbot.send_otp(email,{'username':username,'name':name})
            mongo.db.otp.insert_one({"username":username,"otp":otp})
            params ={'title':'Reset Password','verify':False,'username':username}
            return render_template('middle_page.html',params=params)
        else:
            page_not_found(Exception)
    else:
        return 'Hello World'

@app.route('/otp/<username>',methods=['GET','POST'])
def otp(username):
    '''
        Checks validity of the OTP and sends mail to the user.
    '''
    if request.method == 'POST':
        mailbot = mailingbot()
        otp = request.form['otp']
        otp_db = mongo.db.otp.find_one({'username': username})['otp']
        password_user = mongo.db.test_collection.find_one({'username': username})['password']
        email_user = mongo.db.test_collection.find_one({'username': username})['email']
        name_user = mongo.db.test_collection.find_one({'username': username})['name']
        valid = mailbot.validate_otp(otp_db,otp)
        print(valid)
        print(otp)
        print(otp_db)
        if valid:
            mailbot.send_password(email_user,{'name':name_user,'username':username,'password':password_user})
            mongo.db.otp.delete_one({'username': username})
            return redirect("/login")
        else:
            return page_not_found(Exception)


if __name__ == '__main__':
    app.run(debug=True)