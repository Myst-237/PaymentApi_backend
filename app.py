from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

#database model configuration
class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    codeRef = db.Column(db.String(50))
    isValid = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'codeRef for {self.code} is {self.codeRef} - {self.isValid}'

#start a webdriver     
def start_driver():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    options = webdriver.ChromeOptions()
    #options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    return uc.Chrome(
        options=options
    )
    
#bot to send a phone number to egifter.com and recieve a verfication
def send_phone_number_bot(driver, amount, phoneNumber):
    driver.get("https://www.egifter.com/")
    appleCard = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div.HomeCardCatalogComponent > div > div > div > div.mt-4 > div > div > div:nth-child(4) > div > div.brandImageContainer.rounded-top.overflow-hidden > div > div"))
    )
    script0 = 'let appleCard = document.querySelector("#main-content > div > div.HomeCardCatalogComponent > div > div > div > div.mt-4 > div > div > div:nth-child(4) > div > div.brandImageContainer.rounded-top.overflow-hidden > div > div"); appleCard.click()'
    time.sleep(0.5)
    driver.execute_script(script0)
    amountInput = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[1]/div[2]/div/div/section[1]/div/div/div[2]/form/div[1]/div/div/div/div/div/div[2]/div[2]/div/input'))
    )
    for i in range(0,5):
        amountInput.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
    amountInput.send_keys(amount)
    script1 = 'let forMyselfButton = document.querySelector("#main-content > div > div.BrandBodyComponent.ITUNESC > div.ContainerComponent.container.container-sm.brandDetailsContainer.container-max-width-xl > div > div > section.my-6 > div > div > div.BrandFormComponent > form > section:nth-child(5) > div > div:nth-child(1) > button"); forMyselfButton.click()'
    time.sleep(0.5)
    driver.execute_script(script1)
    proceedToCheckout = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div/div[1]/div[2]/div/div/div[2]/section[2]/div/button[2]'))
    )
    script2 = 'let proceedToCheckout = document.querySelector("#main-content > div > div > div.ContainerComponent.container.container-sm.HeadlineLayoutComponent.CartComponent.container-max-width-xl.ribbonedHeadlineEnabled > div.card.contentWrapper.bg-white > div > div > div.mt-4.mt-xl-0.col-xl-6 > section:nth-child(3) > div > button.eg-button.mdc-button.mdc-button--raised.eg-button--block.mdc-ripple-upgraded.eg-button--variant-primary"); proceedToCheckout.click()'
    time.sleep(1)
    driver.execute_script(script2)
    continueAsGuest = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/section[2]/button'))
    )
    script3 = 'let continueAsGuest = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > section.mt-2 > button"); continueAsGuest.click()'
    time.sleep(1)
    driver.execute_script(script3)
    creditCard = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[1]/div/button'))
    )
    script4 = 'let creditCard = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div:nth-child(1) > div > button"); creditCard.click()'
    time.sleep(1)
    driver.execute_script(script4)
    numberInput = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/form/div/div/div[1]/input'))
        )
    time.sleep(1)
    numberInput.send_keys(phoneNumber)
    script5 = 'let sendCode = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > div > form > div > button"); sendCode.click()'
    time.sleep(1)
    driver.execute_script(script5)

#bot to send the verification code received     
def send_verification_code_bot(driver, verificationCode):
    confirmCodeInput = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/form/div/div[2]/div[1]/div[1]/div/div[1]/input'))
    )
    time.sleep(1)
    confirmCodeInput.send_keys(verificationCode)
    script0 = 'let verifyNumber = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > div > form > div > div:nth-child(3) > div.mt-2 > button"); verifyNumber.click()'
    time.sleep(1)
    driver.execute_script(script0)
    
    
#this function takes in as parameter the reference for a verification code, searches for the code in the database for "timeDelay"seconds
#then returns the verification which can be the codeObject or a None object
def get_verification_code_object(codeRef, timeDelay):
    found = False
    count = 0
    verificationCodeObject = ''
    while not found:
        verificationCodeObject = VerificationCode.query.filter_by(codeRef=codeRef).first()
        if verificationCodeObject is not None:
            found = True
        count = count + 1
        if count == timeDelay:
            break
        time.sleep(1)
    return verificationCodeObject

#this function takes in a verification codeObject and returns a boolean to determine if it is valid or not after "timeDelay"seconds
def code_is_valid(codeRef):
    verificationCodeObject1 = VerificationCode.query.filter_by(codeRef=codeRef).first()
    valid = verificationCodeObject1.isValid
    return valid
    
 #api endpoint incharge of taking the phonenumber,amount and sending the verification code  
@app.route('/send-phone-number', methods=["POST"])
@cross_origin()
def send_phone_number():
    driver = start_driver()
    amount = int(request.json["amount"])
    phoneNumber = request.json["phoneNumber"]
    codeRef = request.json["codeRef"]
    #the code should take approximately 20seconds to reach here
    send_phone_number_bot(driver,amount, phoneNumber)
    #get the verification code send by the user
    verificationCodeObject = get_verification_code_object(codeRef, 60)
    #if the user send the verifation code after 60 seconds
    if verificationCodeObject is not None:  
        #validate the code
        send_verification_code_bot(driver,verificationCodeObject.code)  
        time.sleep(10) #time to see the result in headfull mode
        driver.quit()
        verificationCodeObject.isValid = True
        db.session.commit()
        return jsonify({'response': 'OK'})
    else:
        return jsonify({'response': 'NO'})

    
@app.route('/save-code', methods=["POST"])
@cross_origin()
def save_verification_code_to_db():
    verificationCode = request.json["verificationCode"]
    codeRef = request.json["codeRef"]
    verificationCodeObject = VerificationCode(code=verificationCode, codeRef=codeRef)
    db.session.add(verificationCodeObject)
    db.session.commit()
    return jsonify({'response': 'OK'})

    
@app.route('/validate-code', methods=["POST"])
@cross_origin()
def validate_code():
    codeRef = request.json["codeRef"]
    verificationCodeObject = VerificationCode.query.filter_by(codeRef=codeRef).first()
    if verificationCodeObject is not None:
        return jsonify({'codeFound': True,'valid': verificationCodeObject.isValid})
    else:
        return jsonify({'codeFound': False, 'valid': False})
    
    
@app.route('/send-payment-details', methods=["POST"])
@cross_origin()
def send_payment_details():
    codeRef = request.json["codeRef"]
    verificationCodeObject = VerificationCode.query.filter_by(codeRef=codeRef).first()
    if verificationCodeObject is not None:
        return jsonify({'codeFound': True,'valid': verificationCodeObject.isValid})
    else:
        return jsonify({'codeFound': False, 'valid': False})
    

        


if __name__ == '__main__':
    app.run(debug=True)
