#model class file for users.
import sys,os,hashlib,random,string
sys.path.append(os.path.abspath(os.path.join('../')))
from resources.user_crud import *
from resources.sendmail import send_smtpmail
import logging

class User:
    @classmethod
    def __init__(self,data):
        self.bbid=data['bbid']
        self.password = data['password']        #password is hash(salt+password)
        self.email = data['email']
        self.preferences = data['preferences']
        self.code = data['code']
        self.salt = data['salt']
        self.active = data['active']

    def to_dict(self):
        return {
            'bbid': self.bbid,
            'password': self.password,
            'email': self.email,
            'preferences': self.preferences,
            'code': self.code,
            'salt': self.salt,
            'active': self.active
        }
def gen_salt(n):
    if n==6:
        salt=''.join(random.choices(string.digits, k=n)) #only use digits for code.
    else:
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    return salt

def hash_password(password):
    try:
        hash=hashlib.sha256(password.encode()).hexdigest()
        logging.debug('Password hashed successfully',hash)
        return hash
    except Exception as e:
        logging.error(str(e))
        raise Exception('Password hashing failed')
    
def insert_user(data):
    data['bbid'] = 'bb'+str(get_id())
    data['code'] = gen_salt(6)             #create a verification code and store it in the db
    data['salt'] = gen_salt(16)            #create a salt and store it in the db.
    data['password'] = hash_password(data['password']+data['salt']) #create hash after salting.
    data['active'] = False                 #account inactive until verification code is entered.
    message = f"Subject: Book Barter Registration\n\nDear User,\n\nThank you for registering with Book Barter. Your registration is successful. Please use the following code to activate your account.\n\nActivation Code: {data['code']}\n\nThank you,\nBook Barter Team"
    send_smtpmail(data['email'], message)  #send the email with verification code to the user.
    usr = User(data)
    return insert_userdb(usr)

#set up another endpoint to verify the code and activate the user.
def verify_user(data):
    email = data['email']
    code = data['code']
    query = {'email': email, 'code': code}
    try:
        res=find_userdb(query) #returns a User object
        if res.email == email and res.code == code:
            res.active = True
            res.code = None
        data={'code':res.code,'active':res.active}        #only update code and active fields.
        query={'bbid':res.bbid}
        if update_userdb(query,data)==1:
            return True
        return False
    #Handle NoneType object returned by find_userdb
    except AttributeError as e:
        logging.error(str(e))
        raise Exception("User doesn't exist or already verified")
    except Exception as e:
        logging.error(str(e))
        raise Exception('User verification failed')
    
def find_user(query):
    email = query['email']
    password = query['password']
    query = {'email': email}
    try:
        res=find_userdb(query)
        if res.password == hash_password(password+res.salt) and res.active:
            return True, res.bbid
        elif res.active == False:
            raise Exception('User not verified')
        else:
            raise Exception('Invalid credentials')
    except AttributeError as e:
        logging.error(str(e))
        raise Exception("Invalid Credentials") #Error message shouldn't reveal if user exists or not.

'''When a user requests a password reset, the system should generate a code and send it to the user's email address.
   But the active field or password should not be changed. The code should be stored in the db and sent to the user.
   Only when the user enters the correct code, the password should be reset.
'''
def pwrst_code(data): 
    email = data['email']
    query = {'email': email}
    try:
        res=find_userdb(query)
        if res.email == email:
            res.code = gen_salt(6)
        data={'code':res.code}        #only update code
        query={'bbid':res.bbid}
        if update_userdb(query,data)==1:
            message = f"Subject: Book Barter Password Reset\n\nDear User,\n\nYou have requested a password reset. Please use the following code to reset your password.\n\nReset Code: {res.code}\n\nThank you,\nBook Barter Team"
            send_smtpmail(res.email, message)  #send the email with verification code to the user.
            return True
        return False
    except AttributeError as e:
        logging.error(str(e))
        raise Exception("Verification code sent, if User exists") #Error message shouldn't reveal if user exists or not.
    except Exception as e:
        logging.error(str(e))
        raise Exception('Password reset failed')

def pwrst(data):
    email = data['email']
    password = data['password']
    code=data['code']
    query = {'email': email}
    try:
        res=find_userdb(query)
        if res.code is None:
            raise Exception('No pending password reset request')
        elif res.code==code:
            res.code=None
            res.password = hash_password(password+res.salt)
            data={'password':res.password,'code':res.code}        #only update password and code fields.
            query={'bbid':res.bbid}
            logging.debug('Password reset successful')
            if update_userdb(query,data)==1:
                return True
        return False
    except AttributeError as e:
        logging.error(str(e))
        raise Exception("Invalid user Credentials") #Error message shouldn't reveal if user exists or not.
    except Exception as e:
        logging.error(str(e))
        raise Exception('Password reset failed')