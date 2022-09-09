import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from app.models import VerificationCode
from app.models import Otp
from app.models import PhoneNumber
from app.models import CardDetails
from app import db


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

#start a webdriver     
def start_driver():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
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
    options.add_argument('--lang=en_US')
    return uc.Chrome(
        options=options,
        #version_main=104,
        executable_path = os.environ.get("CHROMEDRIVER_PATH")
    )
    
#bot to send a phone number and amount to egifter.com and recieve a verfication code
def send_phone_number_bot(driver, amount, phoneNumber):
    try:
        print('1')
        driver.get("https://www.egifter.com")
        print('2')
        #make browser window active
        for i in range(0,10):
            ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(0.1)
        print('3')
        appleCard = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="BrandCard_ITUNESC"]'))
        )
        script0 = 'let appleCard = document.querySelector(\'[data-testid="BrandCard_ITUNESC"]\'); appleCard.click()'
        time.sleep(1)
        driver.execute_script(script0)
        print('4')
        amountInput = WebDriverWait(driver,10).until( 
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="DenominationSelector_AmountInputField"]'))
        )
        ActionChains(driver).move_to_element(amountInput).click().perform()
        for i in range(0,6):
            amountInput.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
        ActionChains(driver).move_to_element(amountInput).send_keys(amount).perform()
        time.sleep(0.5)
        ActionChains(driver).move_to_element(amountInput).send_keys(Keys.TAB).perform()
        
        forMyselfButton = WebDriverWait(driver,10).until( 
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="BrandForm_Digital_BuyForMyselfButton"]'))
        )
        script1 = 'let forMyselfButton = document.querySelector(\'[data-testid="BrandForm_Digital_BuyForMyselfButton"]\'); forMyselfButton.click()'
        driver.execute_script(script1)
     
        proceedToCheckout = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="Cart_CartActions_ProceedToCheckoutButton"]'))
        )
        script2 = 'let proceedToCheckout = document.querySelector(\'[data-testid="Cart_CartActions_ProceedToCheckoutButton"]\'); proceedToCheckout.click()'
        time.sleep(0.5)
        driver.execute_script(script2)
        
        continueAsGuest = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="Checkout_GuestCheckoutNotice_ContinueAsGuestButton"]'))
        )
        script3 = 'let continueAsGuest = document.querySelector(\'[data-testid="Checkout_GuestCheckoutNotice_ContinueAsGuestButton"]\'); continueAsGuest.click()'
        time.sleep(0.5)
        driver.execute_script(script3)
        
        creditCard = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PaymentTilesContainer_PaymentMethodButton_CreditCard"]'))
        )
        script4 = 'let creditCard = document.querySelector(\'[data-testid="PaymentTilesContainer_PaymentMethodButton_CreditCard"]\'); creditCard.click()'
        time.sleep(0.5)
        driver.execute_script(script4)
        
        numberInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PhoneVerification_PhoneNumberInputField"]'))
            )
        time.sleep(0.5)
        numberInput.send_keys(phoneNumber)
    
        sendCode = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PhoneVerification_SendCodeButton"]'))
        )
        script5 = 'let sendCode = document.querySelector(\'[data-testid="PhoneVerification_SendCodeButton"]\'); sendCode.click()'
        time.sleep(0.5)
        driver.execute_script(script5)
        
        confirmCodeInput = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PhoneVerification_VerificationCodeInputField"]'))
        )
        
        return True
    except Exception as e:
        driver.quit()
        return False


#bot to send the verification code received     
def send_verification_code_bot(driver, verificationCode):
    try:
        confirmCodeInput = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PhoneVerification_VerificationCodeInputField"]'))
        )
        time.sleep(0.5)
        confirmCodeInput.send_keys(verificationCode)
        
        verifyNumber = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PhoneVerification_VerifyPhoneNumberButton"]'))
        )
        script0 = 'let verifyNumber = document.querySelector(\'[data-testid="PhoneVerification_VerifyPhoneNumberButton"]\'); verifyNumber.click()'
        time.sleep(0.5)
        driver.execute_script(script0)
        
        nameOnCardInput = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="CreditCardFormPartial_CardholderNameInputField"]'))
        )
        
        return True
    except Exception as e:
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
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="CreditCardFormPartial_CardholderNameInputField"]'))
        )
        nameOnCardInput.send_keys(cardDetails.cardHolderName)
        time.sleep(1)
        
        cardNumberInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="CreditCardFormPartial_CardNumberInputField"]'))
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
        time.sleep(1)
        
        cvvInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="CreditCardFormPartial_CardCVVInputField"]'))
        )
        cvvInput.send_keys(cardDetails.cvv)
        time.sleep(1)
        
        addressLine1Input = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AddressFormPartial_AddressLine1InputField"]'))
        )
        addressLine1Input.send_keys(cardDetails.addressLine1)
        time.sleep(1)
        
        addressLine2Input = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AddressFormPartial_AddressLine2InputField"]'))
        )
        addressLine2Input.send_keys(cardDetails.addressLine2)
        time.sleep(1)
        
        cityInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AddressFormPartial_CityInputField"]'))
        )
        cityInput.send_keys(cardDetails.city)
        time.sleep(1)
        
        usStateNumber = us_state[cardDetails.state]
        script2 = 'let stateButton = document.querySelector("#main-content > div > div.card.contentWrapper.bg-white > div > div.row > div.mt-4.mt-xl-0.col-xl-6 > div.PaymentMethodsSectionComponent > div > div > div > div > div > div > div.paymentFormWrapper > div:nth-child(3) > div > div > form > section:nth-child(2) > div > div.row > div.col-8 > div > div.eg-select.mdc-select.mdc-select--filled > div.mdc-select__menu.mdc-menu.mdc-menu-surface > ul > li:nth-child('+usStateNumber+') > a"); stateButton.click()'
        driver.execute_script(script2)
        time.sleep(1)
        
        zipInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AddressFormPartial_ZipCodeInputField"]'))
        )
        zipInput.send_keys(cardDetails.zip)
        time.sleep(1)
        
        emailInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="ConfirmEmailInput_FirstEmailInputField"]'))
        )
        emailInput.send_keys('soniccoastls@gmail.com')
        time.sleep(1)
        
        emailConfirmInput = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="ConfirmEmailInput_SecondEmailInputField"]'))
        )
        emailConfirmInput.send_keys('soniccoastls@gmail.com')
        time.sleep(1)
        
        script3 = 'checkoutButton = document.querySelector(\'[data-testid="Checkout_Form_CheckoutButton"]\'); checkoutButton.click()'
        driver.execute_script(script3)
        time.sleep(1)
        
        otpInputOROrderConfirm = WebDriverWait(driver,20).until(EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#Cardinal-ElementContainer')),
                EC.presence_of_element_located((By.CSS_SELECTOR, '.OrderSummaryComponent'))
            ))
        
        return True
    except Exception as e:
        driver.quit()
        return False


#bot to send_otp_code received
def send_otp_bot(driver, code):
    try:
        otpInput = WebDriverWait(driver,10).until(
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
        driver.quit()
        return False
    

def initiate_payment_process(amount, phoneNumber, codeRef, cardRef):
    driver = start_driver()
    try:
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
                            #verify if otp is needed by looking for the order confirmation div in this case the order summary component
                            OrderSummaryComponent = driver.find_elements(By.CSS_SELECTOR, ".OrderSummaryComponent")
                            lengthOfElementArray = len(OrderSummaryComponent)
                            #if the length of the div is greater than 0 then the order has been confirmed
                            if (lengthOfElementArray > 0):
                                driver.quit()
                                return 'Payment is Validating, It may take a few minutes to be approved. You will be notified once our process review is completed'
                            else:
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
                                        return 'Payment is Validating, It may take a few minutes to be approved. You will be notified once our process review is completed'
                                    else:
                                        driver.quit()
                                        return 'Failed to validate OTP, The otp entered may be incorrect'
                                else:
                                    driver.quit()
                                    return 'OTP Timeout, if your card uses otp verification,  please contact your card issuer to fix any problems'
                        else:
                            driver.quit()
                            return 'A Problem Occured while Validating Payment Details,Verify your card is valid, contains sufficient funds and try again'
                    else:
                        driver.quit()
                        return 'Payment Timeout: Timeouts occur after 10 minutes without any request'    
                else:
                    driver.quit()
                    return 'Code is not valid, The verification code entered is invalid'
            else:
                driver.quit()
                return 'Verification Code Timeout: Timeouts occur after 10 minutes without any request'
        else:
            driver.quit()
            return 'A Problem Occured while Validating Phone number, Please Try again'
    finally:
        driver.quit()