#  important libraries
import os
import pickle
from datetime import datetime
from werkzeug.utils import secure_filename
import base64
import codecs
import gridfs
import json
from urllib2 import urlopen
import requests
import cryptocode

# Flask backend 
from flask import Flask, render_template, request, redirect, session, g 
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage
from flask_migrate import Migrate

# using external classes
from ext_classes import secret_keys
from ext_classes import codes
from ext_classes import mailingbot

sk = secret_keys()
app = Flask(__name__)

app.config["MONGO_URI"] = sk.mongo_uri()
app.secret_key = sk.session()

mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

app.config['TRACK_USAGE_USE_FREEGEOIP'] = True
app.config['TRACK_USAGE_FREEGEOIP_ENDPOINT'] = 'http://extreme-ip-lookup.com/json/'
# app.config['TRACK_USAGE_FREEGEOIP_ENDPOINT'] = 'http://ip-api.com/json/{ip}'
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://sloixhfsqeysdo:c4e589a071b5cfa801b7520308527a6ab527cc283827f1e04f0f1e4b5b1def59@ec2-54-163-97-228.compute-1.amazonaws.com:5432/d2egb1ndgev118"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tracker.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# mstorage = MongoStorage('user','tracker',host='mongodb+srv://testcluster.f7oii.mongodb.net/myFirstDatabase',username='bths',password='BThSProject1.0')
sql_db = SQLAlchemy(app)
migrate = Migrate(app,sql_db)
sstorage = SQLStorage(db=sql_db,table_name='tracker_user')

t = TrackUsage(app,[sstorage])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')


@t.include
@app.route('/',methods=['GET'])
def index():
    with open('track.json','a') as f:
        data = urlopen('http://extreme-ip-lookup.com/{request.remote_addr}/json')
        data = json.load(data)
        json.dump(data,f)
        
    return render_template('home.html')    


@t.include
@app.route('/record',methods=['GET'])
def record():
    if "userid" in session:
        g.track_var['userid'] = session["userid"]

        if session["userid"].startswith("DOC"):
            return render_template('details_form_doc.html')

        elif session['userid'].startswith('ORG'):
            userid = session['userid']
            return render_template('records_form_org.html',userid=userid)

        else:
            return page_not_found(Exception)
    else:
        return redirect('/login')


@t.include
@app.route('/docrecord', methods=['POST','GET'])
def docrecord():
    if "userid" in session:
        g.track_var['userid'] = session["userid"]
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
                advice = request.form['advice']
                advice = advice.replace('\r','').split('\n')
                if doctor_id == session['userid']:
                    p_id = mongo.db.test_collection.find_one({'username': patient_id,'title':'Patient'})
                    if p_id:
                        
                        time_now = datetime.now()
                        id = mongo.db.doc_database.insert_one({
                            'doctorID':doctor_id,
                            'patientID':patient_id,
                            'date':date,
                            'diagnostic':diagnostic,
                            'disease':disease,
                            'advice':advice,
                            'medicines':medicines,
                            'tests':tests,
                            'time_created':time_now
                        })
                        
                        _ = mongo.db.pat_database.insert_one({
                            'id':id.inserted_id,
                            'patientID':patient_id,
                            'type_record':'Doctor',
                            'time_created':time_now,
                            'notified':False
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


@t.include
@app.route('/radrecord', methods=['POST','GET'])
def radrecord():
    if "userid" in session:
        g.track_var['userid'] = session["userid"]
        if session['userid'].startswith('ORGRAD'):
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
                        
                        _ = mongo.db.pat_database.insert_one({
                            'id':id_org.inserted_id,
                            'patientID':patient_id,
                            'type_record':labtype,
                            'time_created':time_now,
                            'notified':False
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


@t.include
@app.route('/pharmanewrecord', methods=['POST','GET'])
def pharmanewrecord():
    if "userid" in session:
        g.track_var['userid'] = session["userid"]
        if session['userid'].startswith('ORGPHA'):
            if request.method == 'POST':
                labtype = "Pharmacy-New-Stock"
                labid = request.form['labid']
                date = request.form['date']
                company_name = request.form['compname']
                medicine_name = request.form['medname']
                quantity = request.form['quantity'].split('*')
                boxes = int(quantity[0])
                strips = int(quantity[1])
                tablets = int(quantity[2])
                tottablets = boxes*strips*tablets
                exp_date = request.form['expdate']
                if labid == session['userid']:
                    time_now = datetime.now()
                    _ = mongo.db.pharma_stock_database.insert_one({
                        'PharmacyID':labid,
                        'PharmaStockType': labtype,
                        'date':date,
                        'company_name':company_name,
                        'medicine_name':medicine_name,
                        'quantity_boxes':boxes,
                        'quantity_strips':strips,
                        'quantity_tablets':tablets,
                        'total_tablets':tottablets,
                        'expiry_date': exp_date,
                        'time_created':time_now
                    })
                    
                    return redirect('/user')
                    
                else:
                    return page_not_found(Exception)
            else:
                return page_not_found(Exception)               
        else:
            return redirect('/user')
    else:
        return redirect('/login')


@t.include
@app.route('/pharmadisrecord', methods=['POST','GET'])
def pharmadisrecord():
    if "userid" in session:
        g.track_var['userid'] = session["userid"]
        if session['userid'].startswith('ORGPHA'):
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
                        
                        _ = mongo.db.pat_database.insert_one({
                            'id':id_pharma.inserted_id,
                            'patientID':patient_id,
                            'type_record':labtype,
                            'time_created':time_now,
                            'notified':False
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
    pass


@t.include
@app.route('/pathorecord', methods=['POST','GET'])
def pathorecord():    
    if "userid" in session:
        g.track_var['userid'] = session["userid"]
        if session['userid'].startswith('ORGPAT'):
            if request.method == 'POST':
                labtype = "Pathology"
                labid = request.form['labid']
                patient_id = request.form['patid']
                date = request.form['date']
                department_name = request.form['dep']
                investigation = request.form['inve'].replace('\r','').split('\n')
                if labid == session['userid']:
                    p_id = mongo.db.test_collection.find_one({'username': patient_id,'title':'Patient'})
                    if p_id:
                        
                        time_now = datetime.now()
                        id_patho = mongo.db.patho_database.insert_one({
                            'LaboratoryID':labid,
                            'Laboratory Type': 'Pathology',
                            'department_name':department_name,
                            'patientID':patient_id,
                            'date':date,
                            'investigations':investigation,
                            'time_created':time_now
                        })
                        
                        _ = mongo.db.pat_database.insert_one({
                            'id':id_patho.inserted_id,
                            'patientID':patient_id,
                            'type_record':labtype,
                            'time_created':time_now,
                            'notified':False
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


@t.include
@app.route('/login', methods=['GET','POST'])
def login():
    '''
        Recieves login credentials from the frontend and sends it to the user function to create session for the user.
    '''
    if request.method == 'POST':
        username = request.form['userid']
        password = request.form['password']        
        userid = mongo.db.test_collection.find_one({"username":username})
        decoded_password = cryptocode.decrypt(userid['password'], sk.password_secret_key())
        # print(password)
        # print(decoded_password)
        if userid and decoded_password == password:
        
            if os.path.exists(os.path.join('cache','activeusers.pkl')):
                with open(os.path.join('cache','activeusers.pkl'),'rb') as f:
                    activeusers = pickle.load(f)
                
                user = activeusers['users']
                
                if username in user:
                    # not logged out but closed the browser
                    
                    if os.path.exists(os.path.join('cache',f'{username}_cache.pkl')):
                        
                        os.remove(os.path.join('cache',f'{username}_cache.pkl'))
                        user.remove(username)
                        

                user.append(username)
                
                activeusers['users'] = user
                with open(os.path.join('cache','activeusers.pkl'),'wb') as f:
                    pickle.dump(activeusers,f)
                

            else:
                if not os.path.exists('cache'):
                    os.mkdir('cache')
                activeusers = dict()
                users = list()
                users.append(username)
                activeusers['users'] = users
                with open(os.path.join('cache','activeusers.pkl'),'wb') as f:
                    pickle.dump(activeusers,f)
                

            session['userid'] = userid['username']
            session["time_first_entry"] = datetime.now()

            user_record = mongo.db.users_activity.find_one({'userid':userid['username']})
            if user_record:
                _ = mongo.db.users_activity.update_one({'userid':userid['username']},{'$addToSet':{'activity':{'title':'login','time':datetime.now()}}})
            else:
                _ = mongo.db.users_activity.insert_one({'userid':userid['username'],'activity':[{'title':'login','time':datetime.now()}]})
                


            return redirect("/user")

        else:
            return page_not_found(Exception)

    else:
        if "userid" in session:
            return redirect("/user")
        return render_template('patient-login-page.html')


@t.include
@app.route('/user')
def user():
    '''
        Creates session for a specific user.
        Retrives all the data related to the users which is being authenticated to it.
        
    '''
        # pat_database -> patient
        # doc_database -> doctor
        # org_database -> radiology
        # pharma_stock_database -> pharmacy
        # patho_database -> pthology

    #security check if user has closed the browser and no data remains in the session  
    

    if "userid" in session:
        g.track_var['userid'] = session["userid"]
        userid = session["userid"]
        user = mongo.db.test_collection.find_one({'username':userid})
        name = user['name']
        city = user['city']
        title = user['title']
        img = fs.get(user['id'])
        base64_data = codecs.encode(img.read(), 'base64')
        image = base64_data.decode('utf-8')

        session['title'] = title
        
        mon_code = codes()

        # Dashboard 1 -> Patient
        if session['title'] == 'Patient':
            
            # 1. using caching property but trying to do it with file system
            # 2. We need to check if there is a new data point then we also need to update it in the dashboard and into the cache memory as well
            # 3. we'll be caching all the records at/before updatedin the databse when the user first enters the dashboard and then we'll be querying the database again based on the timestamp as a keyword 

            if os.path.exists(os.path.join('cache',f'{userid}_cache.pkl')):
                with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
                    data = pickle.load(f)
                meta_data = data['meta_data']
                records = data['data']
                notifications = data['notifications']
                
                

                pat_records = mongo.db.pat_database.find({'patientID':userid,"time_created":{"$gt":session['time_first_entry']}})

                if pat_records:
                    for x in pat_records:
                        notify = dict()
                        if x['type_record'].startswith('Doc'):
                            data = mongo.db.doc_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['doctorID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Appointment'
                                data['heading'] = data['disease']
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                meta_data["appointment"]+=1
                                records.append(data)

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Appointment'
                                    notify['heading'] = data['disease']
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    meta_data['notifications_count']+=1
                                    notifications.append(notify)

                        elif x['type_record'].startswith('Radio'):
                            data = mongo.db.org_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['doctorID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Radiology/Ultrasound'
                                data['heading'] = data['scantype']
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                meta_data["laboratory"]+=1
                                records.append(data)

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Radiology/Ultrasound'
                                    notify['heading'] = data['scantype']
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    meta_data['notifications_count']+=1
                                    notifications.append(notify)

                        elif x['type_record'].startswith('Pharm'):
                            data = mongo.db.pharma_stock_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['PharmacyID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Pharmacy'
                                data['heading'] = 'Medications'
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                meta_data["pharmacy"]+=1
                                records.append(data)

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Pharmacy'
                                    notify['heading'] = 'Medications'
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    meta_data['notifications_count']+=1
                                    notifications.append(notify)

                        elif x['type_record'].startswith('Patho'):
                            data = mongo.db.patho_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['LaboratoryID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Pathology'
                                data['heading'] = data['department_name']
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                meta_data["laboratory"]+=1
                                records.append(data)

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Pathology'
                                    notify['heading'] = data['department_name']
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    meta_data['notifications_count']+=1
                                    notifications.append(notify)
                
                session['time_first_entry'] = datetime.now()

                with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                    pickle.dump({'meta_data':meta_data,'data':records,'notifications':notifications},f)
                
            else:
                if not os.path.exists('cache'):
                    os.mkdir('cache')
                doc_pat_records = 0
                lab_pat_records = 0
                pharma_pat_records = 0
                notifications_count = 0
                records = list()
                notifications = list()
                
                pat_records = mongo.db.pat_database.find({'patientID':userid})
                
                if pat_records:
                    for x in pat_records:
                        notify = dict()
                        if x['type_record'].startswith('Doc'):
                            data = mongo.db.doc_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['doctorID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Appointment'
                                data['heading'] = data['disease']
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                doc_pat_records+=1
                                records.append(data)
                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Appointment'
                                    notify['heading'] = data['disease']
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    notifications_count+=1
                                    notifications.append(notify)

                        elif x['type_record'].startswith('Radio'):
                            data = mongo.db.org_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['doctorID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Radiology/Ultrasound'
                                data['heading'] = data['scantype']
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                lab_pat_records+=1
                                records.append(data)

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Radiology/Ultrasound'
                                    notify['heading'] = data['scantype']
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    notifications_count+=1
                                    notifications.append(notify)

                        elif x['type_record'].startswith('Pharm'):
                            data = mongo.db.pharma_stock_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['PharmacyID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Pharmacy'
                                data['heading'] = 'Medications'
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                records.append(data)
                                pharma_pat_records+=1

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Pharmacy'
                                    notify['heading'] = 'Medications'
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    notifications_count+=1
                                    notifications.append(notify)

                        elif x['type_record'].startswith('Patho'):
                            data = mongo.db.patho_database.find_one({'patientID':userid,'_id':x['id']})
                            if data:
                                doc_name = mongo.db.test_collection.find_one({'username':data['LaboratoryID']})
                                data['doc_name'] = doc_name['name']
                                data['category'] = 'Pathology'
                                data['heading'] = data['department_name']
                                data['mon'] = mon_code.month_codes(data['date'].split('-')[1])
                                data['day'] = data['date'].split('-')[-1]
                                lab_pat_records+=1
                                records.append(data)

                                if not x['notified']:
                                    notify['doc_name'] = doc_name['name']
                                    notify['category'] = 'Pathology'
                                    notify['heading'] = data['department_name']
                                    notify['date'] = data['date']
                                    notify['id'] = x['id']
                                    notifications_count+=1
                                    notifications.append(notify)
            
                meta_data = {'appointment':doc_pat_records,'pharmacy':pharma_pat_records,'laboratory':lab_pat_records,'notifications_count':notifications_count}

                session['time_first_entry'] = datetime.now()

                with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                    pickle.dump({'meta_data':meta_data,'data':records,'notifications':notifications},f)
                
            return render_template('user_dashboard.html',params={"username":userid,"name":name,"city":city,'image':image,'title':title,'meta_data':meta_data,'records':records})


        # Dashboard 2 -> Doctor
        if session['title'] == 'Doctor':
            print('Doctor')
            # pass


        # Dashboard 3 -> Organization
        if session['title'] == 'Organisation':
            type_org = mongo.db.test_collection.find_one({'username':userid,'title':'Organisation'})
            type_org = type_org['organisation_type']
            if type_org.startswith('Pha'):
                if os.path.exists(os.path.join('cache',f'{userid}_cache.pkl')):
                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
                        data = pickle.load(f)
                    meta_data = data['meta_data']
                    records = data['data']                  

                    org_pharma_records = mongo.db.pharma_stock_database.find({'PharmacyID':userid,"time_created":{"$gt":session['time_first_entry']}})

                    if org_pharma_records:
                        for x in org_pharma_records:
                            data = dict()
                            data['type'] = x['PharmaStockType']
                            if x['PharmaStockType'] == "Pharmacy-New-Stock":
                                data['comp'] = x['company_name']
                                data['meds'] = x['medicine_name']
                                data['quan'] = x['total_tablets']
                                data['date'] = x['expiry_date']
                                data['dispdate'] = '-'
                                meta_data["stockpharmacy"]+=1
                                records.append(data)
                            elif x['PharmaStockType'] == "Pharmacy-Dispatched":
                                for i in x['medicines']:
                                    med = i.split('-')
                                    data['comp'] = med[0]
                                    data['meds'] = med[1]
                                    data['quan'] = med[2]
                                    data['date'] = '-'
                                    data['dispdate'] = x['date']

                                meta_data["dispatchedpharmacy"]+=1
                                records.append(data)
                      
                    session['time_first_entry'] = datetime.now()
                    
                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                        pickle.dump({'meta_data':meta_data,'data':records},f)
                    
                else:
                    if not os.path.exists('cache'):
                        os.mkdir('cache')
                    disp_records = 0
                    stock_records = 0
                    records = list()
                    org_pharma_records = mongo.db.pharma_stock_database.find({'PharmacyID':userid})
                    if org_pharma_records:
                        for x in org_pharma_records:
                            data = dict()
                            data['type'] = x['PharmaStockType']
                            if x['PharmaStockType'] == "Pharmacy-New-Stock":
                                data['comp'] = x['company_name']
                                data['meds'] = x['medicine_name']
                                data['quan'] = x['total_tablets']
                                data['date'] = x['expiry_date']
                                data['dispdate'] = '-'
                                stock_records+=1
                                records.append(data)
                            elif x['PharmaStockType'] == "Pharmacy-Dispatched":
                                for i in x['medicines']:
                                    med = i.split('-')
                                    data['comp'] = med[0]
                                    data['meds'] = med[1]
                                    data['quan'] = med[2]
                                    data['date'] = '-'
                                    data['dispdate'] = x['date']

                                disp_records+=1
                                records.append(data)                        
                        
                    
                    meta_data = {'dispatchedpharmacy':disp_records,'stockpharmacy':stock_records}

                    session['time_first_entry'] = datetime.now()

                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                        pickle.dump({'meta_data':meta_data,'data':records},f)
                    
                return render_template('pharma_dashboard.html',params={"username":userid,"name":name,"city":city,'image':image,'title':title,'type':"Pharmacy",'meta_data':meta_data,'records':records})

            elif type_org.startswith('Rad'):
                if os.path.exists(os.path.join('cache',f'{userid}_cache.pkl')):
                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
                        data = pickle.load(f)
                    meta_data = data['meta_data']
                    records = data['data']
                    
                    org_records = mongo.db.org_database.find({'LaboratoryID':userid,"time_created":{"$gt":session['time_first_entry']}})

                    if org_records:
                        for x in org_records:
                            data = x
                            
                            doc_name = mongo.db.test_collection.find_one({'username':x['doctorID']})
                            if doc_name:
                                data['doc_name'] = doc_name['name']
                                if x['scantype'] == "MRI":
                                    data['category'] = 'MRI'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    meta_data['mri']+=1
                                    records.append(data)
                                elif x['scantype'] == "CT-Scan":
                                    data['category'] = 'CT-Scan'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    meta_data['ctscan']+=1
                                elif x['scantype'] == "X-Ray":
                                    data['category'] = 'X-Ray'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    meta_data['xray']+=1
                                elif x['scantype'] == "Ultrasound":
                                    data['category'] = 'UltraSound'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    meta_data['ultra']+=1
                    
                    session['time_first_entry'] = datetime.now()

                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                        pickle.dump({'meta_data':meta_data,'data':records},f)
                    
                else:
                    if not os.path.exists('cache'):
                        os.mkdir('cache')
                    mri_records = 0
                    ctscan_records = 0
                    xray_records = 0
                    ultra_records = 0
                    records = list()
                    org_records = mongo.db.org_database.find({'LaboratoryID':userid})
                    if org_records:
                        for x in org_records:
                            data = x
                            
                            doc_name = mongo.db.test_collection.find_one({'username':x['doctorID']})
                            if doc_name:
                                x['doc_name'] = doc_name['name']
                                if x['scantype'] == "MRI":
                                    data['category'] = 'MRI'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    mri_records+=1
                                    records.append(data)
                                elif x['scantype'] == "CT-Scan":
                                    data['category'] = 'CT-Scan'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    ctscan_records+=1
                                elif x['scantype'] == "X-Ray":
                                    data['category'] = 'X-Ray'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    xray_records+=1
                                elif x['scantype'] == "Ultrasound":
                                    data['category'] = 'UltraSound'
                                    data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    ultra_records+=1
                
                    meta_data = {'xray':xray_records,'ctscan':ctscan_records,'mri':mri_records,'ultra':ultra_records}

                    session['time_first_entry'] = datetime.now()

                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                        pickle.dump({'meta_data':meta_data,'data':records},f)
                    
                return render_template('rad_dashboard.html',params={"username":userid,"name":name,"city":city,'image':image,'title':title,'meta_data':meta_data,'records':records})

            elif type_org.startswith('Pat'):
                if os.path.exists(os.path.join('cache',f'{userid}_cache.pkl')):
                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
                        data = pickle.load(f)
                    meta_data = data['meta_data']
                    records = data['data']
                    
                    org_records = mongo.db.patho_database.find({'LaboratoryID':userid,"time_created":{"$gt":session['time_first_entry']}})
                    if org_records:
                        for x in org_records:
                            data = x
                            
                            pat_name = mongo.db.test_collection.find_one({'username':x['patientID']})
                            if pat_name:
                                data['pat_name'] = pat_name['name']
                                if x['department_name'] == "Biochemistry":
                                    data['category'] = 'Biochemistry'
                                    # data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    meta_data['biochemistry']+=1
                                    records.append(data)
                                elif x['department_name'] == "Hematology":
                                    data['category'] = 'Hematology'
                                    # data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    meta_data['hematology']+=1
                                elif x['department_name'] == "Clinical-Pathology":
                                    data['category'] = 'Clinical-Pathology'
                                    # data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    meta_data['clinical']+=1
                    
                    session['time_first_entry'] = datetime.now()

                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                        pickle.dump({'meta_data':meta_data,'data':records},f)
                    
                else:
                    if not os.path.exists('cache'):
                        os.mkdir('cache')
                    biochemistry_records = 0
                    hematology_records = 0
                    clinical_records = 0
                    records = list()
                    org_records = mongo.db.patho_database.find({'LaboratoryID':userid})
                    if org_records:
                        for x in org_records:
                            data = x
                            
                            pat_name = mongo.db.test_collection.find_one({'username':x['patientID']})
                            if pat_name:
                                data['pat_name'] = pat_name['name']
                                if x['department_name'] == "Biochemistry":
                                    data['category'] = 'Biochemistry'
                                    # data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    biochemistry_records+=1
                                    records.append(data)
                                elif x['department_name'] == "Hematology":
                                    data['category'] = 'Hematology'
                                    # data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    hematology_records+=1
                                elif x['department_name'] == "Clinical-Pathology":
                                    data['category'] = 'Clinical-Pathology'
                                    # data['heading'] = x['bodypart']
                                    data['mon'] = mon_code.month_codes(x['date'].split('-')[1])
                                    data['day'] = x['date'].split('-')[-1]
                                    records.append(data)
                                    clinical_records+=1
                                
                
                    meta_data = {'biochemistry':biochemistry_records,'hematology':hematology_records,'clinical':clinical_records}

                    session['time_first_entry'] = datetime.now()

                    with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
                        pickle.dump({'meta_data':meta_data,'data':records},f)
                    
                return render_template('patho_dashboard.html',params={"username":userid,"name":name,"city":city,'image':image,'title':title,'meta_data':meta_data,'records':records})

        return render_template('user_dashboard.html',params={"username":userid,"name":name,"city":city,'image':image,'title':title,'meta_data':{'appointment':0,'pharmacy':0,'laboratory':0}})

    return redirect('/login')


@t.include
@app.route('/notifications', methods=['GET'])
def notifications():
    if 'userid' in session:
        userid = session['userid']
        with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
            data = pickle.load(f)
        meta_data = data['meta_data']
        notifications = data['notifications']
        return render_template('notifications.html',params={'meta_data':meta_data,'notifications':notifications})
    else:
        return redirect('/login')


@t.include
@app.route('/notified<int:sno>')
def notified(sno):
    if 'userid' in session:
        userid = session['userid']
        with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
            data = pickle.load(f)
        
        records = data['data']
        meta_data = data['meta_data']
        notifications = data['notifications']
        data = notifications[sno-1]
        # print(data)
        _ = mongo.db.pat_database.update_one({'patientID':userid,'id':data['id']},{'$set':{'notified':True}})

        notifications.pop(sno-1)
        meta_data['notifications_count']-=1

        with open(os.path.join('cache',f'{userid}_cache.pkl'),'wb') as f:
            pickle.dump({'meta_data':meta_data,'data':records,'notifications':notifications},f)

        return redirect('/notifications')
    
    else:
        return redirect('/login')



@t.include
@app.route('/patho_record_detail<int:sno>')
def patho_record_detail(sno):
    if 'userid' in session:
        userid = session['userid']
        with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
            data = pickle.load(f)
        
        data = data['data'][sno-1]
        records = list()
        for i in data['investigations']:
            rec = i.split('-')
            recd = dict()
            if len(rec) > 1:
                recd['inves'] = rec[0]
            
                recd['value'] = rec[1]
            
            records.append(recd)
        
        params ={'dep_name':data['department_name'],
                'records':records,
                'date':data['date'],
                'doc_name':data['pat_name']}
        return render_template('patho_record.html',params=params)


@t.include
@app.route('/rad_record_detail<int:sno>')
def rad_record_detail(sno):
    if 'userid' in session:
        g.track_var['userid'] = session["userid"]

        userid = session['userid']
        with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
            data = pickle.load(f)

                
        data = data['data'][sno-1]

        img = fs.get(data['id'])
        base64_data = codecs.encode(img.read(), 'base64')
        image = base64_data.decode('utf-8')


        params ={'date':data['date'],
        'doc_name':data['doc_name'],
                'scantype':data['scantype'],
                'bodypart':data['bodypart'],
                'observation':data['observation'],
                'impressions':data['impressions'],
                'image':image}

        return render_template('rad_record.html',params=params)


@t.include
@app.route('/record_detail<int:sno>')
def record_detail(sno):
    if 'userid' in session:
        g.track_var['userid'] = session["userid"]

        userid = session['userid']
        with open(os.path.join('cache',f'{userid}_cache.pkl'),'rb') as f:
            data = pickle.load(f)
        
        data = data['data'][sno-1]
        

        if data['category'].startswith('App'):
            params = {'doc_name':data['doc_name'],
                    'date':data['date'],
                    'prescription':data['medicines'],
                    'advice':data['advice'],
                    'diagnostic':data['tests']}

            return render_template('record.html',params=params)

        elif data['category'].startswith('Rad'):

            img = fs.get(data['id'])
            base64_data = codecs.encode(img.read(), 'base64')
            image = base64_data.decode('utf-8')


            params ={'date':data['date'],
            'doc_name':data['doc_name'],
                    'scantype':data['scantype'],
                    'bodypart':data['bodypart'],
                    'observation':data['observation'],
                    'impressions':data['impressions'],
                    'image':image}

            return render_template('rad_record.html',params=params)

        elif data['category'].startswith('Pat'):
            
            records = list()
            for i in data['investigations']:
                rec = i.split('-')
                recd = dict()
                if len(rec) > 1:
                    recd['inves'] = rec[0]
                
                    recd['value'] = rec[1]
                
                records.append(recd)
            
            params ={'dep_name':data['department_name'],
                    'records':records,
                    'date':data['date'],
                    'doc_name':data['doc_name']}
            return render_template('patho_record.html',params=params)

        elif data['category'].startswith('Pha'):

            medicines = list()
            for i in data['medicines']:
                med = i.split('-')
                meds = dict()
                
                meds['comp'] = med[0]
                
                meds['meds'] = med[1]
               
                meds['quan'] = med[2]
                
                medicines.append(meds)
            
            params ={'PharmaStockType':data['PharmaStockType'],
                    'medicines':medicines,
                    'date':data['date']}
            return render_template('pharma_pat_record.html',params=params)
    else:
        return redirect('/login')


@t.include
@app.route('/signout')
def signout():
    '''
        Clears the session data and ends the session for the user.
    '''
    if "userid" in session:
        g.track_var['userid'] = session["userid"]
        userid = session['userid']
        session.pop("userid", None)
        session.pop("title", None)
        session.pop("time_first_entry", None)
        
        with open(os.path.join('cache','activeusers.pkl'),'rb') as f:
            activeusers = pickle.load(f)
            
        user = activeusers['users']
        user.remove(userid)
        activeusers['users'] = user
        with open(os.path.join('cache','activeusers.pkl'),'wb') as f:
            pickle.dump(activeusers,f)

        if os.path.exists(os.path.join('cache',f'{userid}_cache.pkl')):
            os.remove(os.path.join('cache',f'{userid}_cache.pkl'))

        _ = mongo.db.users_activity.update_one({'userid':userid},{'$addToSet':{'activity':{'title':'logout','time':datetime.now()}}})
    
    return redirect('/')


@t.include
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
        if title.startswith('Org'):
            orgtype = request.form['orgtype']
            username = title[:3].upper() + orgtype[:3].upper() + code.statecode(state) + dob.split('-')[0] + str(code.usernumber(title,state))

        else:
            username = title[:3].upper() + code.statecode(state) + dob.split('-')[0] + str(code.usernumber(title,state))

        filename = username + '.png'
        
        password_hash = cryptocode.encrypt(password,sk.password_secret_key())

        try:
            if not mongo.db.test_collection.find_one({'adhaar':adhaar}):
                id = mongo.save_file(filename,request.files['photo'])
                
                if title.startswith('Org'):                   
                    orgtype = request.form['orgtype']
                    _ = mongo.db.test_collection.insert_one({"id":id,
                                                    "name":name,
                                                    "dob":dob,
                                                    "gender":gender,
                                                    "title":title,
                                                    "organisation_type":orgtype,
                                                    "username":username,
                                                    "password":password_hash,
                                                    "address":address,
                                                    "state":state,
                                                    "city":city,
                                                    "pin":pin,
                                                    "mobile":mobile,
                                                    "email":email,
                                                    "adhaar":adhaar,
                                                    "profile_photo":filename,
                                                    "time_created":time_created})
                else:
                    
                    _ = mongo.db.test_collection.insert_one({"id":id,
                                                    "name":name,
                                                    "dob":dob,
                                                    "gender":gender,
                                                    "title":title,
                                                    "username":username,
                                                    "password":password_hash,
                                                    "address":address,
                                                    "state":state,
                                                    "city":city,
                                                    "pin":pin,
                                                    "mobile":mobile,
                                                    "email":email,
                                                    "adhaar":adhaar,
                                                    "profile_photo":filename,
                                                    "time_created":time_created})
                
                mailbot = mailingbot()
                mailbot.send_message(email,{'name':name,'username':username})
                params ={'title':'Account Creation','verify':True}
                return render_template('middle_page.html',params=params)
            else:
                page_not_found(Exception)
        except Exception:
            page_not_found(Exception)
    else:
        return page_not_found(Exception)


@t.include
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
            _ = mongo.db.otp.insert_one({"username":username,"otp":otp})
            params ={'title':'Reset Password','verify':False,'username':username}
            return render_template('middle_page.html',params=params)
        else:
            page_not_found(Exception)
    else:
        return 'Hello World'


@t.include
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
        decoded_password = cryptocode.decrypt(password_user, sk.password_secret_key())
        email_user = mongo.db.test_collection.find_one({'username': username})['email']
        name_user = mongo.db.test_collection.find_one({'username': username})['name']
        valid = mailbot.validate_otp(otp_db,otp)
        
        if valid:
            mailbot.send_password(email_user,{'name':name_user,'username':username,'password':decoded_password})
            _ = mongo.db.otp.delete_one({'username': username})
            return redirect("/login")
        else:
            return page_not_found(Exception)


if __name__ == '__main__':
    app.run(debug=False)
