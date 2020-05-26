from apprun import jsonify, dbController


# 주문번호 등록 테스트를 위한 제품리스트 리턴
@app.route("/itemList", methods=["POST"])
def itemList():
    db = dbController.DB()
    try:
        db.execute("SELECT * FROM items_tb;")
        data = db.fetchall_dict()
        return jsonify(result=True, data=data)
    except:
        return jsonify(result=False, msg="잠시후에 시도해 주세요.")
    finally:
        db.close()
