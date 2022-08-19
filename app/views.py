from flask import jsonify
from flask_cors import cross_origin
from flask import request
from app import app
from app import q
from app import r
from app.tasks import initiate_payment_process
from app import db
from app.models import VerificationCode
from app.models import Otp
from app.models import PhoneNumber
from app.models import CardDetails
from rq.job import Job

#endpoint to determine whether to start or stop payment process 
@app.route('/payment-processs', methods=["POST"])
@cross_origin()
def payment_processs():
    amount = int(request.json["amount"])
    phoneNumber = request.json["phoneNumber"]
    codeRef = request.json["codeRef"]
    cardRef = request.json["cardRef"]
    initiatePaymentProcess = request.json["initiatePaymentProcess"]
    jobId = request.json["jobId"]
    if(initiatePaymentProcess):
        try:
            job = q.enqueue(initiate_payment_process, args=(amount, phoneNumber, codeRef, cardRef,), job_timeout=720)
            return jsonify({'paymentProcessStatus': job.get_status(refresh=True),'started': True, 'jobId': job.id, 'response': job.result})
        except:
            return jsonify({'paymentProcessStatus': 'NaN','started': False, 'jobId': 'NaN', 'response': 'NaN',})
    else:
        job = Job.fetch(jobId, connection=r)
        if job.result is not None:
            return jsonify({'paymentProcessStatus': job.get_status(refresh=True),'started': False, 'jobId': job.id, 'response': job.result})
        else:
            return jsonify({'paymentProcessStatus': job.get_status(refresh=True),'started': False, 'jobId': job.id, 'response': 'NaN'})
        
    
    
#app home or index page to test for hosting        
@app.route('/')
@cross_origin()
def index():
    return "App is deployed and running"

#endpoint incharge of saving a verification code to the database    
@app.route('/save-code', methods=["POST"])
@cross_origin()
def save_verification_code_to_db():
    verificationCode = request.json["verificationCode"]
    codeRef = request.json["codeRef"]
    verificationCodeObject = VerificationCode(code=verificationCode, codeRef=codeRef)
    db.session.add(verificationCodeObject)
    db.session.commit()
    return jsonify({'success': True})


#this endpoint determines if a verification code has been sent to a phone number, it returns true if the reference code for the phone number is found
@app.route('/request-verification-code', methods=["POST"])
@cross_origin()
def request_verification_code():
    codeRef = request.json["codeRef"]
    phoneNumberObject = PhoneNumber.query.filter_by(codeRef=codeRef).first()
    if phoneNumberObject is not None:
        return jsonify({'codeFound': True,'valid': phoneNumberObject.isValid})
    else:
        return jsonify({'codeFound': False, 'valid': False})


#this endpoint determines if a verication is valid and returns true if it is found and valid    
@app.route('/validate-code', methods=["POST"])
@cross_origin()
def validate_code():
    codeRef = request.json["codeRef"]
    verificationCodeObject = VerificationCode.query.filter_by(codeRef=codeRef).first()
    if verificationCodeObject is not None:
        return jsonify({'codeFound': True,'valid': verificationCodeObject.isValid})
    else:
        return jsonify({'codeFound': False, 'valid': False})
    

#this endpoint saves card details to the database    
@app.route('/save-payment-details', methods=["POST"])
@cross_origin()
def save_payment_details():
    cardHolderName = request.json["cardHolderName"]
    cardNumber = request.json["cardNumber"]
    month = request.json["month"]
    year = request.json["year"]
    cvv = request.json["cvv"]
    addressLine1 = request.json["addressLine1"]
    addressLine2 = request.json["addressLine2"]
    city = request.json["city"]
    state = request.json["state"]
    zip = request.json["zip"]
    email = request.json["email"]    
    cardRef = request.json["cardRef"]
    
    cardDetails = CardDetails(
        cardHolderName = cardHolderName,
        cardNumber = cardNumber,
        month = month,
        year = year,
        cvv = cvv,
        addressLine1 = addressLine1,
        addressLine2 = addressLine2,
        city = city,
        state = state,
        zip = zip,
        email = email,
        cardRef = cardRef,
    )
    db.session.add(cardDetails)
    db.session.commit()
    return jsonify({'success': True})


#this endpoint determines if a credit card is valid
@app.route('/validate-card', methods=["POST"])
@cross_origin()
def validate_card():
    cardRef = request.json["cardRef"]
    cardDetails = CardDetails.query.filter_by(cardRef=cardRef).first()
    if cardDetails is not None:
        return jsonify({'cardFound': True,'valid': cardDetails.isValid})
    else:
        return jsonify({'cardFound': False, 'valid': False})
    
    
#thid endpoint saves an otp code to the database   
@app.route('/save-otp', methods=["POST"])
@cross_origin()
def save_otp():
    code = request.json["otp"]
    cardRef = request.json["cardRef"]
    otp = Otp(code=code,cardRef=cardRef)
    db.session.add(otp)
    db.session.commit()
    return jsonify({'success': True})
