from flask import Flask, request, after_this_request
from flask_restful import Api, Resource, reqparse
import sqlite3
import traceback

app = Flask(__name__)
api = Api(app)

class UserGetByHouse(Resource):
    def get(self, id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT USERS.USERID, USERS.NAME " +
                            "FROM HOUSES INNER JOIN USERSTOHOUSES ON HOUSES.HOUSEID=USERSTOHOUSES.HOUSEID " +
                            "INNER JOIN USERS ON USERS.USERID=USERSTOHOUSES.USERID " +
                            "WHERE HOUSES.HOUSEID = {0}".format(id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['user_id'] = row[0]
            temp['name'] = row[1]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not find any users for house with id {0}".format(id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class HouseGetByUser(Resource):
    def get(self, id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT HOUSES.HOUSEID, HOUSES.NAME, HOUSES.DESCRIPTION " +
                            "FROM HOUSES INNER JOIN USERSTOHOUSES ON HOUSES.HOUSEID=USERSTOHOUSES.HOUSEID " +
                            "INNER JOIN USERS ON USERS.USERID=USERSTOHOUSES.USERID " +
                            "WHERE USERS.USERID = {0}".format(id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['house_id'] = row[0]
            temp['name'] = row[1]
            temp['description'] = row[2]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any houses for user with id {0}".format(id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data
        return response, 200


class HouseAdd(Resource):
    def post(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        args = request.form
        required_fields = ['user_id','name','description','refresh_unit','refresh_amount','current_phase','current_turn']
        if not all(x in args.keys() for x in required_fields):
            response['message'] = "The fields {0} are required to add a house".format(required_fields)
            response['returncode'] = 500
            return response, 500
        conn = sqlite3.connect('api.db')
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("INSERT INTO HOUSES(NAME,DESCRIPTION,REFRESHUNIT,REFRESHAMOUNT,CURRENTPHASE,CURRENTTURN) " +
                         "VALUES('{0}','{1}','{2}',{3},'{4}',{5})".format(args['name'], args['description'],args['refresh_unit'],args['refresh_amount'],args['current_phase'],args['current_turn']))
            getID = conn.execute('SELECT last_insert_rowid() from HOUSES;');
            id = getID.fetchone()[0]
            conn.execute("INSERT INTO USERSTOHOUSES(USERID,HOUSEID,ISADMIN) VALUES({0},{1},TRUE)".format(args['user_id'],id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added new new House"
        response['response'] = {'id':id, 'name': args['name'], 'description': args['description'], 'refresh_unit': args['refresh_unit'],
                                'refresh_amount': args['refresh_amount'], 'current_phase': args['current_phase'], 'current_turn': args['current_turn']}
        return response, 200

class UserAdd(Resource):
    def post(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        args = request.form
        required_fields = ['name']
        if not all(x in args.keys() for x in required_fields):
            response['message'] = "The fields {0} are required to add a house".format(required_fields)
            response['returncode'] = 500
            return response, 500
        try:
            conn = sqlite3.connect('api.db')
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("INSERT INTO USERS(NAME) " +
                            "VALUES('{0}')".format(args['name']))
            getID = conn.execute('SELECT last_insert_rowid() from USERS;');
            id = getID.fetchone()[0]
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added new new User"
        response['response'] = {'id': id, 'name': args['name']}
        return response, 200

class UserGet(Resource):
    def get(self,id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT * FROM USERS WHERE USERID = {0}".format(id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['user_id'] = row[0]
            temp['name'] = row[1]
            data.append(temp)
        conn.close()
        if len(data) != 1:
            response['message'] = "error finding user with id {0}".format(id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data[0]
        return response, 200

class ChoresGetByHouse(Resource):
    def get(self, id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT CHORES.CHOREID,CHORES.NAME,CHORES.DESCRIPTION,CHORES.CLAIMED,USERS.USERID,USERS.NAME " +
                             "FROM CHORES INNER JOIN HOUSES ON HOUSES.HOUSEID=CHORES.HOUSEID "
                             "JOIN USERS ON USERS.USERID=CHORES.OWNERID " +
                             "WHERE HOUSES.HOUSEID = {0}".format(id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['chore_id'] = row[0]
            temp['name'] = row[1]
            temp['description'] = row[2]
            temp['claimed'] = row[3]
            temp['owner_id'] = row[4]
            temp['owner_name'] = row[5]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any chores for house with id {0}".format(id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class ChoreAdd(Resource):
    def post(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        args = request.form
        required_fields = ['name','description','house_id','owner_id','claimed']
        if not all(x in args.keys() for x in required_fields):
            response['message'] = "The fields {0} are required to add a chore".format(required_fields)
            response['returncode'] = 500
            return response, 500
        try:
            conn = sqlite3.connect('api.db')
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("INSERT INTO CHORES(NAME,DESCRIPTION,HOUSEID,OWNERID,CLAIMED) " +
                            "VALUES('{0}','{1}',{2},{3},{4})".format(args['name'],args['description'],args['house_id'],args['owner_id'],args['claimed']))
            getID = conn.execute('SELECT last_insert_rowid() FROM CHORES;');
            id = getID.fetchone()[0]
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added new new User"
        response['response'] = {'id': id, 'name': args['name'], 'description':args['description'], 'house_id':args['house_id'], 'owner_id':args['owner_id'],'claimed':args['claimed']}
        return response, 200


class AssignChore(Resource):
    def put(self, chore_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        response = {"response": {}, "message": "", "returncode": 200}
        args = request.form
        required_fields = ['user_id']
        if not all(x in args.keys() for x in required_fields):
            response['message'] = "The fields {0} are required to assign a chore".format(required_fields)
            response['returncode'] = 500
            return response, 500
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT CLAIMED FROM CHORES WHERE CHOREID = {0};".format(chore_id))
            claimed = True;
            for row in s:
                claimed = row[0]
            if claimed:
                response['message'] = "Could not assign this chore"
                response['returncode'] = 400
                return response, 400
            conn.execute("UPDATE CHORES SET CLAIMED=TRUE, OWNERID={0} WHERE CHOREID={1}".format(args['user_id'], chore_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added assigned chore {0} to user {1}".format(chore_id, args['user_id'])
        response['response'] = {'user_id':args['user_id'], 'chore_id':chore_id}
        return response, 200

class OfferAdd(Resource):
    def options(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            return response

        return 200;

    def post(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        args = request.get_json()
        required_fields = ['house_id', 'asking_id', 'receiving_id']
        if not all(x in args.keys() for x in required_fields) or (('chores' not in args.keys()) and ('placements' not in args.keys())):
            response['message'] = "The fields {0} are required to add an offer. Received: {1}".format(required_fields,args.keys())
            response['returncode'] = 500
            return response, 500
        args['offeredChores'] = []
        args['offeredPlacements'] = []
        args['house_id'] = int(args['house_id'])
        args['asking_id'] = int(args['asking_id'])
        args['receiving_id'] = int(args['receiving_id'])
        if 'chores' in args.keys():
            for i in range(len(args['chores'])):
                args['chores'][i] = int(args['chores'][i])
        if 'placements' in args.keys():
            for i in range(len(args['placements'])):
                args['placements'][i] = int(args['placements'][i])
        try:
            conn = sqlite3.connect('api.db')
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("INSERT INTO OFFERS(HOUSEID,ASKINGID,RECEIVINGID,STATUS) " +
                         "VALUES({0}, {1}, {2}, 'u')".format(args['house_id'],args['asking_id'],args['receiving_id']))
            getOfferID = conn.execute('SELECT last_insert_rowid() from USERS;')
            offerID = getOfferID.fetchone()[0]

            if 'chores' in args.keys():
                for chore in args['chores']:
                    temp = {"id":chore}
                    s = conn.execute("SELECT * FROM CHORES WHERE CHOREID={0}".format(chore)).fetchone()
                    if s:
                        if (s[4] == args["asking_id"]):
                            temp["offer_side"] = "a"
                        elif (s[4] == args["receiving_id"]):
                            temp["offer_side"] = "r"
                        else:
                            response['message'] = "Chores were formatted incorrectly."
                            response['returncode'] = 500
                            return response, 500
                    else:
                        response['message'] = "Chores were formatted incorrectly."
                        response['returncode'] = 500
                        return response, 500
                    conn.execute("INSERT INTO OFFEREDCHORES(OFFERID,CHOREID,OFFERSIDE) " +
                                 "VALUES({0},{1},'{2}')".format(offerID,chore,temp['offer_side']))
                    getOfferedChoreID = conn.execute('SELECT last_insert_rowid() FROM OFFEREDCHORES;')
                    temp['offered_chore_id'] = getOfferedChoreID.fetchone()[0]
                    args['offeredChores'].append(temp)
            if 'placements' in args.keys():
                for placement in args['placements']:
                    temp = {"id": placement}
                    s = conn.execute("SELECT * FROM CHORES WHERE CHOREID={0}".format(placement)).fetchone()
                    if s:
                        if (s[4] == args["asking_id"]):
                            temp["offer_side"] = "a"
                        elif (s[4] == args["receiving_id"]):
                            temp["offer_side"] = "r"
                        else:
                            response['message'] = "Placements were formatted incorrectly."
                            response['returncode'] = 500
                            return response, 500
                    else:
                        response['message'] = "Placements were formatted incorrectly."
                        response['returncode'] = 500
                        return response, 500
                    conn.execute("INSERT INTO OFFEREDPLACEMENTS(OFFERID,PLACEMENTID,OFFERSIDE) " +
                                 "VALUES({0},{1},'{2}')".format(offerID, placement, temp['offer_side']))
                    getOfferedPlacementID = conn.execute('SELECT last_insert_rowid() FROM OFFEREDPLACEMENT;')
                    temp['offered_placement_id'] = getOfferedPlacementID.fetchone()[0]
                    args['offeredPlacements'].append(temp)
        except Exception as e:
            traceback.print_exc()
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added new new Offer"
        response['response'] = {'offer_id': offerID, 'house_id': args['house_id'], 'asking_id': args['asking_id'],
                                'receiving_id': args['receiving_id'], 'status': 'u','offeredChores':args['offeredChores'], 'offeredPlacements':args['offeredPlacements']}
        if 'chores' in args.keys():
            response['response']['chores'] = args['chores']
        if 'placements' in args.keys():
            response['response']['palcements'] = args['placements']
        return response, 200

class OffersGetByHouseandUser(Resource):
    def get(self,house_id,user_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute(
                "SELECT * FROM OFFERS " +
                "WHERE HOUSEID={0} AND (ASKINGID={1} OR RECEIVINGID={1});".format(house_id,user_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['offer_id'] = row[0]
            temp['house_id'] = row[1]
            temp['asking_id'] = row[2]
            temp['receiving_id'] = row[3]
            temp['status'] = row[4]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any orders for house with id {0} and user with id {1}".format(house_id,user_id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class OfferedChoresGetByOffer(Resource):
    def get(self,offer_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute(
                "SELECT * FROM OFFEREDCHORES WHERE OFFERID={0};".format(offer_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['order_id'] = row[0]
            temp['chore_id'] = row[1]
            temp['offer_side'] = row[2]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any chores for offer with id {0}".format(offer_id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class OfferAccept(Resource):
    def options(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            return response

        return 200;

    def post(self, offer_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}

        try:
            conn = sqlite3.connect('api.db')
            conn.execute("PRAGMA foreign_keys = ON;")
            offer_res = conn.execute("SELECT * FROM OFFERS WHERE OFFERID={0}".format(offer_id)).fetchall()
            if len(offer_res) == 0:
                response['message'] = "The Offer has been deleted or does not exist"
                response['returncode'] = 404
                return response, 404
            offer = {}
            for row in offer_res:
                offer['offer_id'] = row[0]
                offer['house_id'] = row[1]
                offer['asking_id'] = row[2]
                offer['receiving_id'] = row[3]
                offer['status'] = row[4]
            s = conn.execute("SELECT OFFEREDCHORES.CHOREID,CHORES.OWNERID FROM OFFEREDCHORES JOIN CHORES ON OFFEREDCHORES.CHOREID=CHORES.CHOREID WHERE OFFEREDCHORES.OFFERID={0};".format(offer_id))
            choresInOffer = []
            for row in s:
                if(row[1] == offer['asking_id']):
                    conn.execute("UPDATE CHORES SET OWNERID={0} WHERE CHOREID={1}".format(offer['receiving_id'],row[0]))
                elif(row[1] == offer['receiving_id']):
                    conn.execute("UPDATE CHORES SET OWNERID={0} WHERE CHOREID={1}".format(offer['asking_id'],row[0]))
                choresInOffer.append(row[0])
            conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0}".format(offer_id))
            conn.execute("DELETE FROM OFFERS WHERE OFFERID={0}".format(offer_id))

            offersDeleted = []
            for chore in choresInOffer:
                s = conn.execute("SELECT OFFERID FROM OFFEREDCHORES WHERE CHOREID={0}".format(chore))
                for row in s:
                    conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0}".format(row[0]))
                    conn.execute("DELETE FROM OFFERS WHERE OFFERID={0}".format(row[0]))
                    offersDeleted.append(row[0])

        except Exception as e:
            traceback.print_exc()
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added new new Offer"
        response['response'] = {'offersAffected': offersDeleted}
        return response, 200

class OfferReject(Resource):
    def delete(offer_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}

        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute(
                "SELECT * FROM OFFEREDCHORES WHERE OFFERID={0};".format(offer_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['order_id'] = row[0]
            temp['chore_id'] = row[1]
            temp['offer_side'] = row[2]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any chores for offer with id {0}".format(offer_id)
            response['returncode'] = 400
            return response, 400
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class NotificationsGetByUser(Resource):
    def get(self,user_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT * FROM NOTIFICATIONS WHERE USERID={0} AND ISREAD=FALSE;".format(user_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['notification_id'] = row[0]
            temp['title'] = row[1]
            temp['description'] = row[2]
            temp['is_read'] = row[3]
            temp['user_id'] = row[4]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any chores for offer with id {0}".format(offer_id)
            response['returncode'] = 200
            return response, 200
        response['message'] = "search successful"
        response['response'] = data
        return response, 200




api.add_resource(UserAdd, "/adduser")
api.add_resource(HouseAdd, "/addhouse")
api.add_resource(HouseGetByUser, "/gethousesbyuser/<int:id>")
api.add_resource(UserGet, "/getuser/<int:id>")
api.add_resource(ChoresGetByHouse, "/getchoresbyhouse/<int:id>")
api.add_resource(ChoreAdd, "/addchore")
api.add_resource(UserGetByHouse, "/getusersbyhouse/<int:id>")
api.add_resource(AssignChore, "/assignchore/<int:chore_id>")
api.add_resource(OfferAdd, "/addoffer")
api.add_resource(OffersGetByHouseandUser, "/getoffersbyhouseanduser/<int:house_id>/<int:user_id>")
api.add_resource(OfferedChoresGetByOffer, "/getofferedchoresbyoffer/<int:offer_id>")
api.add_resource(OfferAccept, "/acceptoffer/<int:offer_id>")
api.add_resource(NotificationsGetByUser, "/getnotificationsbyuser/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')