from app import db

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