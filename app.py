from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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
    code = db.Column(db.String(20))
    codeRef = db.Column(db.String(20))
    isValid = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'{self.codeRef} - {self.code} - {self.isValid}'
    
class CardDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardHolderName = db.Column(db.String(100))
    cardNumber = db.Column(db.String(30))
    month = db.Column(db.String(20))
    year = db.Column(db.String(20))
    cvv = db.Column(db.String(20))
    addressLine1 = db.Column(db.String(200))
    addressLine2 = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.String(20))
    email = db.Column(db.String(200))
    cardRef = db.Column(db.String(20))
    
    def __repr__(self):
        return f'{self.cardHolderName} - {self.cardNumber}'
    


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
    try:
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
        return True
    except Exception as e:
        print(e)
        return False

#bot to send the verification code received     
def send_verification_code_bot(driver, verificationCode):
    try:
        confirmCodeInput = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/form/div/div[2]/div[1]/div[1]/div/div[1]/input'))
        )
        time.sleep(1)
        confirmCodeInput.send_keys(verificationCode)
        script0 = 'let verifyNumber = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > div > form > div > div:nth-child(3) > div.mt-2 > button"); verifyNumber.click()'
        time.sleep(1)
        driver.execute_script(script0)
        notification = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(63) > div:nth-child(2) > div > div > div.Vue-Toastification__toast-component-body > span'))
        )
        notification_data = notification.get_attribute('innerHTML')
        print(notification_data)
        if notification_data == 'Success! Your phone number was successfully verified.':
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
 
    
#bot to send card details received 
def send_card_details_bot(driver, cardDetails):
    monthDictionary = {
         '01': '1',
         '02': '2',
         '03': '3',
         '04': '4',
         '05': '5',
         '06': '6',
         '07': '7',
         '08': '8',
         '09': '9',
         '10': '10',
         '11': '11',
         '12': '12'
     }  
    yearDictionary = {
         '2022': '1',
         '2023': '2',
         '2024': '3',
         '2025': '4',
         '2026': '5',
         '2027': '6',
         '2028': '7',
         '2029': '8',
         '2030': '9',
         '2031': '10',
         '2032': '11',
         '2033': '12',
    }
    us_state = {
        'Alabama': '1',
        'Alaska': '2',
        'Arizona': '3',
        'Arkansas': '4',
        'California': '5',
        'Colorado': '6',
        'Connecticut': '7',
        'Delaware': '8',
        'District of Columbia': '9',
        'Florida': '10',
        'Georgia': '11',
        'Hawaii': '12',
        'Idaho': '13',
        'Illinois': '14',
        'Indiana': '15',
        'Iowa': '16',
        'Kansas': '17',
        'Kentucky': '18',
        'Louisiana': '19',
        'Maine': '20',
        'Maryland': '21',
        'Massachusetts': '22',
        'Michigan': '23',
        'Minnesota': '24',
        'Mississippi': '25',
        'Missouri': '26',
        'Montana': '27',
        'Nebraska': '28',
        'Nevada': '29',
        'New Hampshire': '30',
        'New Jersey': '31',
        'New Mexico': '32',
        'New York': '33',
        'North Carolina': '34',
        'North Dakota': '35',
        'Ohio': '36',
        'Oklahoma': '37',
        'Oregon': '38',
        'Pennsylvania': '39',
        'Rhode Island': '40',
        'South Carolina': '41',
        'South Dakota': '42',
        'Tennessee': '43',
        'Texas': '44',
        'Utah': '45',
        'Vermont': '46',
        'Virginia': '47',
        'Washington': '48',
        'West Virginia': '49',
        'Wisconsin': '50',
        'Wyoming': '51'
    }
    try:
        nameOnCardInput = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[1]/div/div[2]/div[1]/div[1]/input'))
        )
        nameOnCardInput.send_keys(cardDetails.cardHolderName)
        time.sleep(1)
        cardNumberInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[1]/div/div[2]/div[2]/div[1]/input'))
        )
        cardNumberInput.send_keys(cardDetails.cardNumber)
        time.sleep(1)
        script0 = f'let monthButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section.row.bg-gray-lighter.py-2 > div > div.CreditCardFormComponent > div.row.flex-nowrap.align-items-center > div:nth-child(1) > div > div.eg-select.mdc-select.mdc-select--filled > div.mdc-select__menu.mdc-menu.mdc-menu-surface > ul > li:nth-child({monthDictionary[cardDetails.month]}) > a; monthButton.click()'
        driver.execute_script(script0)
        time.sleep(1)
        script1 = f'let yearButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section.row.bg-gray-lighter.py-2 > div > div.CreditCardFormComponent > div.row.flex-nowrap.align-items-center > div.px-0.col-4 > div > div.eg-select.mdc-select.mdc-select--filled.mdc-select--focused.mdc-select--activated > div.mdc-select__menu.mdc-menu.mdc-menu-surface.mdc-menu-surface--open > ul > li:nth-child({yearDictionary[cardDetails.year]}) > a"); yearButton.click()'
        driver.execute_script(script1)
        cvvInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[1]/div/div[2]/div[3]/div[3]/div/div[1]/input'))
        )
        cvvInput.send_keys(cardDetails.cvv)
        time.sleep(1)
        addressLine1Input = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[2]/div/div[1]/div[1]/input'))
        )
        addressLine1Input.send_keys(cardDetails.addressLine1)
        time.sleep(1)
        addressLine2Input = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[2]/div/div[2]/div/input'))
        )
        addressLine2Input.send_keys(cardDetails.addressLine1)
        time.sleep(1)
        addressLine2Input = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[2]/div/div[2]/div/input'))
        )
        addressLine2Input.send_keys(cardDetails.addressLine2)
        time.sleep(1)
        cityInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[2]/div/div[3]/div[1]/input'))
        )
        cityInput.send_keys(cardDetails.city)
        time.sleep(1)
        script2 = f'let stateButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section:nth-child(2) > div > div.row > div.col-8 > div > div.eg-select.mdc-select.mdc-select--filled.mdc-select--focused.mdc-select--activated > div.mdc-select__menu.mdc-menu.mdc-menu-surface.mdc-menu-surface--open > ul > li:nth-child({us_state[cardDetails.state]}) > a")'
        driver.execute_script(script2)
        time.sleep(1)
        zipInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[2]/div/div[4]/div[2]/div/div[1]/input'))
        )
        zipInput.send_keys(cardDetails.zip)
        time.sleep(1)
        emailInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/div/div[1]/div[1]/input'))
        )
        emailInput.send_keys('fakealexismartin237@gmail.com')
        time.sleep(2)
        script3 = 'checkoutButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section.mt-2 > button"); checkoutButton.click()'
        driver.execute_script(script3)
        time.sleep(1)
        
        return True
    except Exception as e:
        print(e)
        return False
    
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

#this function takes in as parameter the reference for a card details, searches for the code in the database for "timeDelay"seconds
#then returns the card which can be the cardDetail or a none object
def get_card_details(cardRef, timeDelay):
    found = False
    count = 0
    cardDetails = ''
    while not found:
        cardDetails = CardDetails.query.filter_by(cardRef=cardRef).first()
        if cardDetails is not None:
            found = True
        count = count + 1
        if count == timeDelay:
            break
        time.sleep(1)
    return cardDetails

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
    cardRef = request.json["cardRef"]
    #the code should take approximately 20seconds to reach here
    phone_number_sent = send_phone_number_bot(driver,amount, phoneNumber)
    if phone_number_sent:
        #get the verification code send by the user
        verificationCodeObject = get_verification_code_object(codeRef, 300)
        #if the user send the verifation code after 60 seconds
        if verificationCodeObject is not None:  
            #validate the code
            code_is_valid = send_verification_code_bot(driver,verificationCodeObject.code)  
            if code_is_valid:
                verificationCodeObject.isValid = True
                db.session.commit()
                #get the card details sent by the user
                cardDetails = get_card_details(cardRef, 300)
                print(cardDetails)
                if cardDetails is not None:
                    card_details_sent = send_card_details_bot(driver,cardDetails)
                    if card_details_sent:
                        time.sleep(10) #time to see the result in headfull mode
                        driver.quit()
                        return jsonify({'success': True})
                    else:
                        return jsonify({'success': False, 'message': 'failed to send card Details'})
                else:
                    return jsonify({'success': False, 'message': 'failed to send card details'})    
            else:
                return jsonify({'success': False, 'message': 'phone number is not valid'})
        else:
            return jsonify({'success': False, 'message': 'No verification code found'})
    else:
        return jsonify({'success': False, 'message': 'failed to send phone number'})

    
@app.route('/save-code', methods=["POST"])
@cross_origin()
def save_verification_code_to_db():
    verificationCode = request.json["verificationCode"]
    codeRef = request.json["codeRef"]
    verificationCodeObject = VerificationCode(code=verificationCode, codeRef=codeRef)
    db.session.add(verificationCodeObject)
    db.session.commit()
    return jsonify({'success': True})

    
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
    print(cardDetails.cardRef)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
