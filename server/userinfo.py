from apprun import dbController, request, jsonify

# 단일 회원 상세 정보 조회 API
@app.route("/userInfo", methods=["POST"])
def userInfo():
    user = request.json
    res, msg, data = service_userInfo(user)
    return jsonify(result=res, msg=msg, data=data)


# 단일 회원 상세 정보 조회 함수
def service_userInfo(user):
    id = user.get("id", "")
    db = dbController.DB()
    try:
        sql = """
        SELECT
            `id`,
            `name`,
            `nickname`,
            `telnum`,
            `email`,
            CASE
                WHEN `gender` = 0 THEN "남자"
                WHEN `gender` = 1 THEN "여자"
                ELSE "설정 안 함" END AS gender
        FROM user_tb
        WHERE `id`=%(id)s;
        """
        db.execute(sql, {"id": id})
        user_info = db.fetchone_dict()
        if user_info:
            return True, "{0}님의 정보입니다.".format(user_info["name"]), user_info
        else:
            return False, "정보를 찾을 수 없습니다.", ''
    except:
        return False, "잠시 후에 시도해 주세요.", ''
    finally:
        db.close()
        