import re

def checkSpaceBar(data):
    reg = re.compile(r'\s')
    try:
        return str(data) if not reg.search(data) else False
    except:
        return False

def idReg(id):
    reg = re.compile('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]')
    return True if not reg.search(id) else False

def passwordReg(pwd):
    return re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&#_.`~])[A-Za-z\d$@$!%*?)&#_.`~]{10,}", pwd)

def nicknameReg(nickname):
    chk = re.search('[a-z]+', nickname)
    if not chk: return False
    return nickname == chk.group()

def emailReg(email):
    return re.search('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$', email)
