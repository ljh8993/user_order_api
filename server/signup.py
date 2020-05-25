from hashlib import sha512
from flask import jsonify, request

import service
import dbController


# 회원가입 API
@app.route("/signup", methods=["POST"])
def signup():
    signup_data = request.json
    res, msg = service_Signup(signup_data)
    return jsonify(result=res, msg=msg)

# 회원가입 함수
def service_Signup(user):
    pwd1, pwd2 = user.get("pwd1", ""), user.get("pwd2", "")
    if pwd1 and pwd2 and pwd1 != pwd2:
        return False, "비밀번호와 비밀번호 확인이 일치하지 않습니다."

    signdata = {
        "id": service.checkSpaceBar(user.get("id", "")),
        "pwd": service.checkSpaceBar(pwd1),
        "name": service.checkSpaceBar(user.get("name", "")),
        "nickname": service.checkSpaceBar(user.get("nickname", "")),
        "telnum": service.checkSpaceBar(user.get("telnum", "")),
        "email": service.checkSpaceBar(user.get("email", ""))
    }

    for v in signdata.values():
        if not v:
            return False, "공백을 제거해 주세요."
    
    if not service.idReg(signdata["id"]):
        return False, "아이디는 ( _ )를 제외한 특수문자를 사용할 수 없습니다."

    if len(signdata["pwd"]) < 10:
        return False, "비밀번호는 최소 10자 이상으로 설정해 주세요."

    if len(signdata["name"]) > 20:
        return False, "이름은 20자 이하로 설정해 주세요."

    if len(signdata["nickname"]) > 30:
        return False, "별명은 30자 이하로 설정해 주세요."
    
    if len(signdata["telnum"]) > 20 or not signdata["telnum"].isdecimal():
        return False, "적합한 전화번호를 작성해 주세요."

    if len(signdata["email"]) > 100 or not service.emailReg(signdata["email"]):
        return False, "적합한 E-mail형식으로 작성해 주세요."

    if not signdata["name"].isalpha():
        return False, "이름은 한글 및 영문으로 작성해 주세요."

    if not service.nicknameReg(signdata["nickname"]):
        return False, "별명은 영어 소문자로만 작성해 주세요."
    
    if not service.passwordReg(signdata["pwd"]):
        return False, "비밀번호는 영문 대/소문자, 숫자, 특수문자가 1개 이상 포함되어야 합니다."
    else:
        signdata["pwd"] = sha512(signdata["pwd"].encode('utf-8')).hexdigest()
        
    gender_chk = user.get("gender", None)
    
    db = dbController.DB()

    try:
        db.execute("SELECT COUNT(*) FROM user_tb WHERE `id`=%(id)s", {"id": signdata["id"]})
        cnt = db.fetchone()[0]
        if cnt > 0:
            return False, "중복된 아이디입니다."

        key_sql = """
            INSERT INTO user_tb (
                `id`, `pwd`, `name`, `nickname`, `telnum`, `email`, `signup_date`
        """
        
        val_sql = """
            ) VALUES (
                %(id)s, %(pwd)s, %(name)s, %(nickname)s, %(telnum)s, %(email)s, NOW()
        """
        if gender_chk is not None and gender_chk.isdecimal() and gender_chk in ["0", "1"]:
            signdata["gender"] = int(gender_chk)
            key_sql += ", `gender`"
            val_sql += ", %(gender)s"

        sql = key_sql + val_sql + ");"
        db.execute(sql, signdata)
        db.commit()
        return True, "정상적으로 회원가입 되었습니다."
    except:
        db.rollback()
        return False, "잠시 후에 시도해 주세요."
    finally:
        db.close()
