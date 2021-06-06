import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import json
from email.utils import make_msgid
import math
import random

class codes:
    def statecode(self,state):
        load_dotenv()
        codes = json.loads(os.getenv('STATECODES'))
        state = state.lower()
        return codes[state]

    def usernumber(self,title,state):
        with open('codes.json','r') as json_file:
            if(json_file.readlines()) != 0:
                json_file.seek(0)
                codes = json.loads(json_file.read())
        title = title.lower()
        state = state.lower()
        print(codes)
        if title.startswith('pat'):
            code = codes["PATIENTCODES"][state] + 1
            codes["PATIENTCODES"][state] = code
            with open('codes.json','w') as json_file:
                json.dump(codes, json_file)
            return code
        if title.startswith('doc'):
            code = codes["DOCTORCODES"][state] + 1
            codes["DOCTORCODES"][state] = code
            with open('codes.json','w') as json_file:
                json.dump(codes, json_file)
            return code
        if title.startswith('org'):
            code = codes["ORGANISATIONCODES"][state] + 1
            codes["ORGANISATIONCODES"][state] = code
            with open('codes.json','w') as json_file:
                json.dump(codes, json_file)
            return code

class secret_keys:
    def __init__(self):
        load_dotenv()

    def session(self):
        return os.getenv('SESSION_SECRET_KEY')

    def mongo_uri(self):
        return os.getenv('MONGO_URI')

class mailingbot:
    def __init__(self):
        load_dotenv()
        EMAIL = os.getenv('EMAIL')
        PASSWORD = os.getenv('PASSWORD')
        otp_string = os.getenv('OTPSTRING')
        self.email = EMAIL
        self.password = PASSWORD
        self.otpstring = otp_string
        self.otp = ""

    def otp_generator(self,len_otp):

        OTP = ""
        length = len(self.otpstring)
        for i in range(len_otp) :
            OTP += self.otpstring[math.floor(random.random() * length)]
    
        return OTP

    def send_message(self, reciever, message):
        # we need to change the format as we are going to send certian credentials 

        msg = EmailMessage()
        
        asparagus_cid = make_msgid()
        msg.add_alternative(f"""\
                            <html>
                                <head></head>                                
                                <body style='font-size=15px;'>
                                    
                                    <p>
                                        Hi <strong>{message['name']}</strong>,<br>
                                    </p>
                                    <p>
                                        Welcome to <strong>...</strong>, <br>
                                        We thank you for choosing our services.<br>
                                        Your User ID is <strong>{message['username']}</strong>.<br>
                                        Your Password is <strong> same as you set during the registration process</strong>.
                                    </p>
                                    <p>
                                    Warm Regards, <br>
                                    Customer Care <br>
                                    ___
                                    </p>
                                    
                                    <p>
                                        <hr>
                                        <strong>
                                            This is a system generated mail. Please do not reply to this email id. <br>If you have a query or need any clarification you may:<br>
                                            Email us at <a href='\'style='text-decoration:none;'>__</a>
                                        </strong>
                                        <hr>
                                    </p>

                                </body>
                            </html>
                            """.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

        msg['from'] = self.email
        msg['to'] = reciever
        msg['subject'] = f' {message["name"]} Form Submission '
        
        print(msg)
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, reciever, msg.as_string())
            smtp.quit()

            print(" Mail sent successfully! ")
        except Exception:
            raise Exception(" Your mail was not sent successfully ")

    def send_password(self, reciever, message):
        # we need to change the format as we are going to send certian credentials 

        msg = EmailMessage()
        
        asparagus_cid = make_msgid()
        msg.add_alternative(f"""\
                            <html>
                                <head></head>                                
                                <body style='font-size=15px;'>
                                   
                                    <p>
                                        Hi <strong>{message['name']}</strong>,<br>
                                    </p>
                                    <p>
                                        <strong>You have successfully recovered your Password.</strong>
                                        For User ID is <strong>{message['username']}</strong>.<br>
                                        Password is <strong> {message['password']}</strong>.
                                    </p>
                                    <p>
                                    Warm Regards, <br>
                                    Customer Care <br>
                                    ___
                                    </p>
                                     
                                    <p>
                                        <hr>
                                        <strong>
                                            This is a system generated mail. Please do not reply to this email id. <br>If you have a query or need any clarification you may:<br>
                                            Email us at <a href='\'style='text-decoration:none;'>__</a>
                                        </strong>
                                        <hr>
                                    </p>
                                </body>
                            </html>
                            """.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

        msg['from'] = self.email
        msg['to'] = reciever
        msg['subject'] = f' {message["name"]} Password '
        
        print(msg)
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, reciever, msg.as_string())
            smtp.quit()

            print(" Mail sent successfully! ")
        except Exception:
            raise Exception(" Your mail was not sent successfully ")
    
    def send_otp(self, reciever,message):

        self.otp = self.otp_generator(6)

        # we need to change the format as we are going to send certian credentials 

        msg = EmailMessage()
        
        asparagus_cid = make_msgid()
        msg.add_alternative(f"""\
                            <html>
                                <head></head>                                
                                <body style='font-size=15px;'>
                                    
                                    <p>
                                        Hi <strong>{message['name']}</strong>,<br>
                                    </p>
                                    <p>
                                        Your One Time Password(OTP) for recovering your password : <br>
                                        For User ID  <strong>{message['username']}</strong>.<br>
                                        Your OTP is <strong> {self.otp} </strong>.
                                    </p>
                                    <p>
                                    Warm Regards, <br>
                                    Customer Care <br>
                                    ___
                                    </p>
                                    
                                    <p>
                                        <hr>
                                        <strong>
                                            This is a system generated mail. Please do not reply to this email id. <br>If you have a query or need any clarification you may:<br>
                                            Email us at <a href='\'style='text-decoration:none;'>__</a>
                                        </strong>
                                        <hr>
                                    </p>
                                </body>
                            </html>
                            """.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

        msg['from'] = self.email
        msg['to'] = reciever
        msg['subject'] = f' {message["name"]} Reset Password OTP '
        
        print(msg)
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, reciever, msg.as_string())
            smtp.quit()

            print(" Mail sent successfully! ")
        except Exception:
            raise Exception(" Your mail was not sent successfully ")

        return self.otp

    def validate_otp(self,otp_db,otp):
        if otp_db == otp:
            return True
        return False

if __name__ == '__main__':
    mail = mailingbot()
    # mail.send_message('vp037453@gmail.com',{'name':'Vivek Prasad','username':"DOCBH211"})
    # otp_db = mail.send_otp('vp037453@gmail.com',{'name':'Vivek Prasad','username':"DOCBH211"})
    mail.send_password('vp037453@gmail.com',{'name':'Vivek Prasad','username':"DOCBH211","password":"Helloavjobye"})
    # otp = input()
    # print(mail.validate_otp(otp_db,otp))
    # code = codes()
    # print(code.usernumber("Patient","Assam"))
    pass