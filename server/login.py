from apprun import jsonify, session, request, dbController
from hashlib import sha512


# 로그아웃 API
@app.route("/logout", methods=["POST"])
def logout():
    if "u_id" in session:
        del session["u_id"]
    return jsonify(result=True, msg="로그아웃 되었습니다.")

# 로그인 API
@app.route("/login", methods=["POST"])
def login():
    login_data = request.json
    res, msg = service_Login(login_data)
    if res:
        session["u_id"] = login_data["id"]
    return jsonify(result=res, msg=msg)

# 로그인 함수
def service_Login(user):
    login_id = user.get("id", None)
    login_pwd = user.get("pwd", None)
    if not login_id:
        return False, "아이디를 입력해 주세요."
    if not login_pwd:
        return False, "비밀번호를 입력해 주세요."

    login_data = {
        "id": login_id,
        "pwd": sha512(login_pwd.encode('utf-8')).hexdigest()
    }

    db = dbController.DB()

    try:
        db.execute("SELECT COUNT(*) FROM user_tb WHERE `id`=%(id)s AND `pwd`=%(pwd)s", login_data)
        cnt = db.fetchone()[0]
        if cnt == 1:
            return True, "로그인 되었습니다."
        return False, "올바른 계정을 입력해 주세요."
        
    except:
        return False, "잠시 후에 시도해 주세요."
    finally:
        db.close()
        