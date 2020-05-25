from flask import jsonify, session, request
from datetime import datetime as dt
from hashlib import sha256

import dbController


# 제품 구매 시 order_attribute_tb(주문속성테이블)에 데이터 등록을 위한 API
## 주문번호 생성을 위함
@app.route("/orderItem", methods=["POST"])
def orderItem():
    idx = request.json.get('idx', 0) # 제품리스트인 items_tb의 idx를 받아옴
    if "u_id" not in session:
        return jsonify(result=False, msg="재 로그인을 해주세요.")
    u_id = session["u_id"]
    res, msg = service_OrderItems(idx, u_id)
    return jsonify(result=res, msg=msg)


# 구매한 제품 DB에 등록
def service_OrderItems(idx, uid):
    if not idx:
        return False, "제품을 선택해 주세요."
    
    db = dbController.DB()

    try:
        db.execute("SELECT COUNT(*) FROM user_tb WHERE `id`=%(id)s", {"id": uid})
        cnt = db.fetchone()[0]
        if not cnt:
            return False, "없는 아이디입니다."
        
        db.execute("SELECT `name` FROM items_tb WHERE `idx`=%(idx)s", {"idx": idx})
        item_name = db.fetchone_dict()
        if not item_name or not item_name.get("name", None):
            return False, "제품이 준비 중에 있습니다.<br/>잠시만 기다려 주세요."
        item_name = item_name["name"]

        made_orderNum = makeOrderNum(db, idx)
        if not made_orderNum: # 주문번호 생성 10회 반복해도 중복이 된다면 잠시 후 시도해 달라는 요청 리턴
            return False, "잠시 후에 시도해 주세요."
        
        data = {
            "order_num": made_orderNum,
            "order_id": uid,
            "item_name": item_name,
            "item_idx": idx
        }

        sql = """
            INSERT INTO order_attribute_tb(
                `order_num`, `order_id`, `item_name`, `item_idx`, `payment_date`
            ) VALUES (
                %(order_num)s, %(order_id)s, %(item_name)s, %(item_idx)s, NOW()
            );
        """
        db.execute(sql, data)
        db.commit()
        return True, f"주문번호 : {made_orderNum}<br/>이용해 주셔서 감사합니다."
    except:
        db.rollback()
        return False, "잠시 후에 시도해 주세요."
    finally:
        db.close()

# 주문번호 생성
def makeOrderNum(db, idx):
    from time import sleep
    for _ in range(10):
        date = dt.now().strftime("%Y%m%d%H%M%S.%f")
        made_order_num = date[1:6] + sha256(date[6:].encode("utf-8")).hexdigest()[2:9].upper()
        cnt = db.execute("SELECT COUNT(*) FROM order_attribute_tb WHERE `order_num`=%(made_order_num)s", {"made_order_num": made_order_num})
        if not cnt:
            return made_order_num
        sleep(0.01)

    return False
    