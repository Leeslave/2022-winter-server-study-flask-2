from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    def get(self):
        # GET method 구현 부분
        database = Database()
        id = request.args.get("id")
        pw = request.args.get("password")
        sql = database.execute_one(f"SELECT * FROM user WHERE id = '{id}';")
        if sql == None:
            # 없음
            database.close()
            return {"message" : "해당 유저가 존재하지 않음"}, 400
        else:
            # 아이디 비밀번호 확인
            if sql['pw'] != pw:
                database.close()
                return {"message" : "아이디나 비밀번호 불일치"}, 400
            else:
                database.close()
                return {"nickname" : sql['nickname']}, 200
                

    def put(self):
        # PUT method 구현 부분
        database = Database()
        data = request.get_json()
        sql = database.execute_one(f"SELECT * FROM user WHERE id = '{data['id']}';")
        if sql == None:
            # 없음
            database.close()
            return {"is_success" : False,"message" : "아이디나 비밀번호 불일치"}, 400
        else:
            if sql['pw'] != data['password']:
                database.close()
                return {"is_success" : False,"message" : "아이디나 비밀번호 불일치"}, 400
            elif sql['nickname'] == data['nickname']:
                database.close()
                return {"is_success" : False,"message" : "현재 닉네임과 같음"}, 400
            
            else:
                database.execute(f"UPDATE user SET nickname = '{data['nickname']}';")
                database.commit()
                database.close()
                return {"is_success" : True, "message" : "유저 닉네임 변경 성공"}, 200

    def post(self):
        # POST method 구현 부분
        database = Database()
        data = request.get_json()
        sql = database.execute_one(f"SELECT * FROM user WHERE id = '{data['id']}';")
        if sql == None:
            query = (f"INSERT INTO user VALUES ('{data['id']}','{data['password']}','{data['nickname']}');")
            database.execute(query)
            database.commit()
            database.close()
            return {"is_success" : True, "message" : "유저 생성 성공"}, 200
        else : 
            database.close()
            return {"is_success" : False, "message" : "이미 있는 유저"}, 400

    
    def delete(self):
        # DELETE method 구현 부분
        database = Database()
        data = request.get_json()
        sql = database.execute_one(f"SELECT * FROM user WHERE id = '{data['id']}';")
        if sql == None:
            # 없음
            database.close()
            return {"is_success" : False,"message" : "아이디나 비밀번호 불일치"}, 400
        else:
            if sql['pw'] != data['password']:
                database.close()
                return {"is_success" : False,"message" : "아이디나 비밀번호 불일치"}, 400
            else:
                database.execute(f"DELETE FROM user WHERE id = '{data['id']}';")
                database.commit()
                database.close()
                return {"is_success" : True, "message" : "유저 삭제 성공"}, 200
