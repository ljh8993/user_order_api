from flask import jsonify, request

import dbController

# 여러 회원 목록 조회 API
@app.route("/userSInfo", methods=["POST"])
def userSInfo():
    data = request.json
    res, data = service_userSInfo(data)
    if res:
        return jsonify(result=True, data=data)
    return jsonify(result=False, msg=data)


# 여러 회원 목록 조회 함수
def service_userSInfo(data):
    # 한 페이지당 20명의 회원 반환으로 정의
    # 이름, 이메일로 검색 가능
    chk = data.get("chk", None) # '0' == 모든리스트, '1' == 이름 검색, '2' == 이메일 검색
    if chk is None:
        return False, "구분을 정해 주세요."

    page = data.get("page", 0)
    page, chk = str(page), str(chk)

    if not page or not page.isdecimal() or int(page) < 1:
        return False, "페이지를 선택해 주세요."

    page = int(page)-1
    search = data.get("search", "")
    
    db = dbController.DB()

    try:
        where = ""
        if chk == '1':
            where = "WHERE a.`name` LIKE '%%{}%%'".format(search)
        elif chk == '2':
            where = "WHERE a.`email` LIKE '%%{}%%'".format(search)

        sql = """
            SELECT
                a.`id`,
                a.`name`,
                a.`nickname`,
                a.`telnum`,
                a.`email`,
                CASE
                    WHEN a.`gender` = 0 THEN "남자"
                    WHEN a.`gender` = 1 THEN "여자"
                    ELSE "설정 안 함" END AS gender,
                DATE_FORMAT(
                    (SELECT MAX(b.payment_date) FROM order_attribute_tb b WHERE a.`id`=b.`order_id`),
                    '%Y-%m-%d %H:%i:%s'
                ) AS payment_date
            FROM user_tb a
            {0}
            LIMIT {1}, {2};
        """.format(where, page*20, 20)
        db.execute(sql)
        data = db.fetchall_dict()
        return True, data
    except:
        return False, "잠시 후에 시도해 주세요."
    finally:
        db.close()