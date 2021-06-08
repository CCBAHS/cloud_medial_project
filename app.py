# Flask backend 
from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import base64
import codecs
import gridfs
from ext_classes import secret_keys
from ext_classes import codes
from ext_classes import mailingbot

sk = secret_keys()
app = Flask(__name__)

app.config["MONGO_URI"] = sk.mongo_uri()
app.secret_key = sk.session()

mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')


@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/record',methods=['GET'])
def record():
    if "userid" in session:
        if session["userid"].startswith("DOC"):
            return render_template('details_form_doc.html')
        elif session['userid'].startswith('ORG'):
            return render_template('records_form_org.html')
        else:
            return page_not_found(Exception)
    else:
        return redirect('/login')

@app.route('/docrecord', methods=['POST','GET'])
def docrecord():
    if "userid" in session:
        if session['userid'].startswith('DOC'):
            if request.method == 'POST':
                doctor_id = request.form['docid']
                patient_id = request.form['patid']
                date = request.form['date']
                diagnostic = request.form['diag']
                diagnostic = diagnostic.replace('\r','').split('\n')
                disease = request.form['dise']
                tests = request.form['tests']
                tests = tests.replace('\r','').split('\n')
                medicines = request.form['meds']
                medicines = medicines.replace('\r','').split('\n')
                if doctor_id == session['userid']:
                    p_id = mongo.db.test_collection.find_one({'username': patient_id,'title':'Patient'})
                    if p_id:
                        print(doctor_id)
                        print(patient_id)
                        print(date)
                        print(diagnostic)
                        print(disease)
                        print(tests)
                        print(medicines)
                        time_now = datetime.now()
                        id = mongo.db.doc_database.insert_one({
                            'doctorID':doctor_id,
                            'patientID':patient_id,
                            'date':date,
                            'diagnostic':diagnostic,
                            'disease':disease,
                            'medicines':medicines,
                            'tests':tests,
                            'time_created':time_now
                        })
                        print("Doctors")
                        print(id.inserted_id)
                        mongo.db.pat_database.insert_one({
                            'id':id.inserted_id,
                            'patientID':patient_id,
                            'type_record':'Doctor',
                            'time_created':time_now
                        })
                        return redirect('/user')
                    else:
                        return page_not_found(Exception)
                else:
                    return page_not_found(Exception)
            else:
                return page_not_found(Exception)              
        else:
            return redirect('/user')
    else:
        return redirect('/login')

@app.route('/radrecord', methods=['POST','GET'])
def radrecord():
    if "userid" in session:
        if session['userid'].startswith('ORG'):
            if request.method == 'POST':
                labtype = "Radiological/Ultrasound"
                labid = request.form['labid']
                doctor_id = request.form['docid']
                patient_id = request.form['patid']
                date = request.form['date']
                scantype = request.form['scan']
                bodypart = request.form['bodypart']
                observation = request.form['obvs']
                observation  = observation.replace('\r','').split('\n')
                impressions = request.form['impr']
                impressions = impressions.replace('\r','').split('\n')
                filename = patient_id + ''.join(bodypart.split(' ')) + scantype + ''.join(date.split('-')) + '.png'
                if labid == session['userid']:
                    p_id = mongo.db.test_collection.find_one({'username': patient_id,'title':'Patient'})
                    d_id = mongo.db.test_collection.find_one({'username': doctor_id,'title':'Doctor'})
                    if p_id and d_id:
                        id = mongo.save_file(filename,request.files['scanfile'])
                        print(' Profile Image Saved Successfully')
                        print(doctor_id)
                        print(patient_id)
                        print(filename)
                        print(date)
                        print(scantype)
                        print(bodypart)
                        print(observation)
                        print(impressions)
                        time_now = datetime.now()
                        id_org = mongo.db.org_database.insert_one({
                            'id':id,
                            'LaboratoryID':labid,
                            'Laboratory Type':labtype,
                            'doctorID':doctor_id,
                            'patientID':patient_id,
                            'date':date,
                            'scantype':scantype,
                            'bodypart':bodypart,
                            'observation':observation,
                            'impressions':impressions,
                            'img_filename':filename,
                            'time_created':time_now
                        })
                        print("Doctors")
                        print(id_org.inserted_id)
                        mongo.db.pat_database.insert_one({
                            'id':id_org.inserted_id,
                            'patientID':patient_id,
                            'type_record':labtype,
                            'time_created':time_now
                        })
                        return redirect('/user')
                    else:
                        return page_not_found(Exception)
                else:
                    return page_not_found(Exception)
            else:
                return page_not_found(Exception)               
        else:
            return redirect('/user')
    else:
        return redirect('/login')

@app.route('/pharmanewrecord', methods=['POST','GET'])
def pharmanewrecord():
    if "userid" in session:
        if session['userid'].startswith('ORG'):
            if request.method == 'POST':
                labtype = "Pharmacy-New Stock"
                labid = request.form['labid']
                date = request.form['date']
                company_name = request.form['compname']
                medicine_name = request.form['medname']
                quantity = request.form['quantity'].split('*')
                boxes = int(quantity[0])
                strips = int(quantity[1])
                tablets = int(quantity[2])
                tottablets = boxes*strips*tablets
                if labid == session['userid']:
                    
                    print(labtype)
                    print(labid)
                    print(date)
                    print(company_name)
                    print(medicine_name)
                    print(boxes)
                    print(strips)
                    print(tablets)
                    print(tottablets)
                    time_now = datetime.now()
                    mongo.db.pharma_stock_database.insert_one({
                        'PharmacyID':labid,
                        'PharmaStockType': labtype,
                        'date':date,
                        'company_name':company_name,
                        'medicine_name':medicine_name,
                        'quantity_boxes':boxes,
                        'quantity_strips':strips,
                        'quantity_tablets':tablets,
                        'total_tablets':tottablets,
                        'time_created':time_now
                    })
                    print("Data saved into database")
                    return redirect('/user')
                    
                else:
                    return page_not_found(Exception)
            else:
                return page_not_found(Exception)               
        else:
            return redirect('/user')
    else:
        return redirect('/login')

@app.route('/pharmadisrecord', methods=['POST','GET'])
def pharmadisrecord():
    if "userid" in session:
        if session['userid'].startswith('ORG'):
            if request.method == 'POST':
                labtype = "Pharmacy-Dispatched"
                labid = request.form['labid']
                doctor_id = request.form['docid']
                patient_id = request.form['patid']
                date = request.form['date']
                medicines = request.form['dispmeds'].replace('\r','').split('\n')
                if labid == session['userid']:
                    p_id = mongo.db.test_collection.find_one({'username': patient_id,'title':'Patient'})
                    d_id = mongo.db.test_collection.find_one({'username': doctor_id,'title':'Doctor'})
                    if p_id and d_id:
                        print(labtype)
                        print(labid)
                        print(doctor_id)
                        print(patient_id)
                        print(date)
                        print(medicines)
                        time_now = datetime.now()
                        id_pharma = mongo.db.pharma_stock_database.insert_one({
                            'PharmacyID':labid,
                            'PharmaStockType': labtype,
                            'doctorID':doctor_id,
                            'patientID':patient_id,
                            'date':date,
                            'medicines':medicines,
                            'time_created':time_now
                        })
                        print(id_pharma.inserted_id)
                        mongo.db.pat_database.insert_one({
                            'id':id_pharma.inserted_id,
                            'patientID':patient_id,
                            'type_record':labtype,
                            'time_created':time_now
                        })
                        return redirect('/user')
                    else:
                        return page_not_found(Exception)
                else:
                    return page_not_found(Exception)
            else:
                return page_not_found(Exception)               
        else:
            return redirect('/user')
    else:
        return redirect('/login')


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
        session['userid'] = userid['username']

        return redirect("/user")
    else:
        if "userid" in session:
            return redirect("/user")
        return render_template('patient-login-page.html')

@app.route('/user')
def user():
    '''
        Creates session for a specific user.
        Retrives all the data related to the users which is being authenticated to it.
    '''
    if "userid" in session:
        userid = session["userid"]
        user = mongo.db.test_collection.find_one({'username':userid})
        name = user['name']
        city = user['city']
        title = user['title']
        img = fs.get(user['id'])
        base64_data = codecs.encode(img.read(), 'base64')
        image = base64_data.decode('utf-8')
        return render_template('user_dashboard.html',params={"username":userid,"name":name,"city":city,'image':image,'title':title})
    return redirect('/login')

@app.route('/signout')
def signout():
    '''
        Clears the session data and ends the session for the user.
    '''
    if "userid" in session:
        session.pop("userid", None)
    
    return redirect('/')




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
        password = request.form['password-create']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        pin = request.form['pincode']
        mobile = request.form['mobileno']
        email = request.form['emailid']
        adhaar = request.form['adhaar']
        time_created = datetime.now()        
        username = title[:3].upper() + code.statecode(state) + dob.split('-')[0] + str(code.usernumber(title,state))
        filename = username + '.png'
        print(filename)
        try:
            if not mongo.db.test_collection.find_one({'adhaar':adhaar}):
                id = mongo.save_file(filename,request.files['photo'])
                print(' Profile Image Saved Successfully')
                mongo.db.test_collection.insert_one({"id":id,
                                                    "name":name,
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
                params ={'title':'Reset Password','verify':True}
                return render_template('middle_page.html',params=params)
            else:
                page_not_found(Exception)
        except Exception:
            print(Exception)
    else:
        return page_not_found(Exception)

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