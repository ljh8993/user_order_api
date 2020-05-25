from flask import jsonify, request

import dbController


# 단일 회원의 주문 목록 조회 API
@app.route("/orderedList", methods=["POST"])
def orderedList():
    user = request.json
    res, data = service_orderList(user)
    if res:
        return jsonify(result=True, data=data)
    return jsonify(result=False, msg=data)

# 단일 회원의 주문 목록 조회 함수
def service_orderList(user):
    order_id = user.get("id")
    db = dbController.DB()
    try:
        sql = """
        SELECT
            a.`order_num`,
            a.`item_name`,
            b.`name`,
            b.`email`,
            DATE_FORMAT(a.`payment_date`, '%%Y-%%m-%%d %%H:%%i:%%s') AS payment_date
        FROM order_attribute_tb a
        LEFT OUTER JOIN user_tb b
            ON a.`order_id`=b.`id`
        WHERE `order_id`=%(order_id)s;
        """
        db.execute(sql, {"order_id": order_id})
        datas = db.fetchall_dict() or []
        return True, datas
    except:
        return False, "잠시 후에 시도해 주세요."
    finally:
        db.close()
        