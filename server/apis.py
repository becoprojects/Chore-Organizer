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
            s = conn.execute("SELECT HOUSES.HOUSEID, HOUSES.NAME, HOUSES.DESCRIPTION, HOUSES.CURRENTPHASE " +
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
            temp['current_phase'] = row[3]
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
        print(args)
        required_fields = ['house_id', 'asking_id', 'receiving_id']
        if not all(x in args.keys() for x in required_fields) or (('chores' not in args.keys()) and ('placements' not in args.keys())):
            response['message'] = "The fields {0} are required to add an offer. Received: {1}".format(required_fields,args.keys())
            response['returncode'] = 500
            return response, 500
        args['offered_chores'] = []
        args['offered_placements'] = []
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
            getOfferID = conn.execute('SELECT last_insert_rowid() from OFFERS;')
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
                    args['offered_chores'].append(temp)
            if 'placements' in args.keys():
                for placement in args['placements']:
                    temp = {"id": placement}
                    s = conn.execute("SELECT * FROM PLACEMENTS WHERE PLACEMENTID={0}".format(placement)).fetchone()
                    if s:
                        if (s[1] == args["asking_id"]):
                            temp["offer_side"] = "a"
                        elif (s[1] == args["receiving_id"]):
                            temp["offer_side"] = "r"
                        else:
                            traceback.print_exc()
                            response['message'] = "Placements were formatted incorrectly."
                            response['returncode'] = 500
                            return response, 500
                    else:
                        response['message'] = "Placements were formatted incorrectly."
                        response['returncode'] = 500
                        return response, 500
                    print("INSERT INTO OFFEREDPLACEMENTS(OFFERID,PLACEMENTID,OFFERSIDE) " +
                                 "VALUES({0},{1},'{2}')".format(offerID, placement, temp['offer_side']))
                    conn.execute("INSERT INTO OFFEREDPLACEMENTS(OFFERID,PLACEMENTID,OFFERSIDE) " +
                                 "VALUES({0},{1},'{2}')".format(offerID, placement, temp['offer_side']))
                    getOfferedPlacementID = conn.execute('SELECT last_insert_rowid() FROM OFFEREDPLACEMENTS;')
                    temp['offered_placement_id'] = getOfferedPlacementID.fetchone()[0]
                    args['offered_placements'].append(temp)

            conn.execute("INSERT INTO NOTIFICATIONS(TITLE,DESCRIPTION,ISREAD,USERID) " +
                "VALUES('{0}','{1}',FALSE,{2})".format("New Offer","An Offer is waiting for you",args['receiving_id']))
        except Exception as e:
            traceback.print_exc()
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully added new new Offer"
        response['response'] = {'offer_id': offerID, 'house_id': args['house_id'], 'asking_id': args['asking_id'],
                                'receiving_id': args['receiving_id'], 'status': 'u','offered_chores':args['offered_chores'], 'offered_placements':args['offered_placements']}
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
            response['message'] = "could not any offers for house with id {0} and user with id {1}".format(house_id,user_id)
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

        response = {"response": [], "message": "", "returncode": 200}
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
            temp['offer_id'] = row[0]
            temp['chore_id'] = row[1]
            temp['offer_side'] = row[2]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any chores for offer with id {0}".format(offer_id)
            response['returncode'] = 200
            return response, 200
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
            placementsInOffer = []
            for row in s:
                if(row[1] == offer['asking_id']):
                    conn.execute("UPDATE CHORES SET OWNERID={0} WHERE CHOREID={1}".format(offer['receiving_id'],row[0]))
                elif(row[1] == offer['receiving_id']):
                    conn.execute("UPDATE CHORES SET OWNERID={0} WHERE CHOREID={1}".format(offer['asking_id'],row[0]))
                choresInOffer.append(row[0])
            s = conn.execute("SELECT OFFEREDPLACEMENTS.PLACEMENTID, PLACEMENTS.USERID " +
                             "FROM OFFEREDPLACEMENTS JOIN PLACEMENTS ON OFFEREDPLACEMENTS.PLACEMENTID=PLACEMENTS.PLACEMENTID WHERE OFFERID={0};".format(offer_id))
            for row in s:
                if(row[1] == offer['asking_id']):
                    conn.execute("UPDATE PLACEMENTS SET USERID={0} WHERE PLACEMENTID={1}".format(offer['receiving_id'],row[0]))
                    count = conn.execute("SELECT COUNT(*) FROM REVERTPLACEMENTS WHERE PLACEMENTID={0}".format(row[0])).fetchone()[0]
                    if count == 0:
                        conn.execute("INSERT INTO REVERTPLACEMENTS(REVERTTO,PLACEMENTID) VALUES({0},{1});".format(offer['asking_id'],row[0]))
                elif(row[1] == offer['receiving_id']):
                    conn.execute("UPDATE PLACEMENTS SET USERID={0} WHERE PLACEMENTID={1}".format(offer['asking_id'],row[0]))
                    count = conn.execute("SELECT COUNT(*) FROM REVERTPLACEMENTS WHERE PLACEMENTID={0}".format(row[0])).fetchone()[0]
                    if count == 0:
                        conn.execute("INSERT INTO REVERTPLACEMENTS(REVERTTO,PLACEMENTID) VALUES({0},{1});".format(offer['receiving_id'],row[0]))
                placementsInOffer.append(row[0])
            conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0}".format(offer_id))
            conn.execute("DELETE FROM OFFEREDPLACEMENTS WHERE OFFERID={0}".format(offer_id))
            conn.execute("DELETE FROM OFFERS WHERE OFFERID={0}".format(offer_id))

            offersDeleted = []
            for chore in choresInOffer:
                s = conn.execute("SELECT OFFERID FROM OFFEREDCHORES WHERE CHOREID={0}".format(chore))
                for row in s:
                    conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0}".format(row[0]))
                    conn.execute("DELETE FROM OFFEREDPLACEMENTS WHERE OFFERID={0}".format(row[0]))
                    conn.execute("DELETE FROM OFFERS WHERE OFFERID={0}".format(row[0]))
                    offersDeleted.append(row[0])
            for placement in placementsInOffer:
                s = conn.execute("SELECT OFFERID FROM OFFEREDPLACEMENTS WHERE PLACEMENTID={0}".format(placement))
                for row in s:
                    conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0}".format(row[0]))
                    conn.execute("DELETE FROM OFFEREDPLACEMENTS WHERE OFFERID={0}".format(row[0]))
                    conn.execute("DELETE FROM OFFERS WHERE OFFERID={0}".format(row[0]))
                    offersDeleted.append(row[0])
        except Exception as e:
            traceback.print_exc()
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "Successfully accepted Offer"
        response['response'] = {'offersAffected': offersDeleted}
        return response, 200

class OfferReject(Resource):
    def options(self,offer_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
            return response

        return 200;

    def delete(self,offer_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}

        try:
            conn = sqlite3.connect('api.db')
            conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0};".format(offer_id))
            conn.execute("DELETE FROM OFFEREDPLACEMENTS WHERE OFFERID={0};".format(offer_id))
            conn.execute("DELETE FROM OFFERS WHERE OFFERID={0};".format(offer_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "delete successful"
        return response, 200

class NotificationsGetUnseenByUser(Resource):
    def get(self,user_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": [], "message": "", "returncode": 200}
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
            response['message'] = "could not any notifications for user with id {0}".format(user_id)
            response['returncode'] = 200
            return response, 200
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class NotificationsSetSeen(Resource):
    def options(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
            return response

        return 200;

    def put(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}

        args = request.get_json()
        required_fields = ['notification_id_list']
        if not all(x in args.keys() for x in required_fields):
            response['message'] = "The fields {0} are required to add an offer. Received: {1}".format(required_fields,args)
            response['returncode'] = 500
            return response, 500

        try:
            conn = sqlite3.connect('api.db')
            for id in args['notification_id_list']:
                conn.execute("UPDATE NOTIFICATIONS SET ISREAD=TRUE WHERE NOTIFICATIONID={0};".format(id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "put successful"
        return response, 200

class NotificationAdd(Resource):
    def options(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
            return response

        return 200;

    def post(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}

        args = request.get_json()
        required_fields = ['title','description','user_id']
        if not all(x in args.keys() for x in required_fields):
            response['message'] = "The fields {0} are required to add an offer. Received: {1}".format(required_fields,args)
            response['returncode'] = 500
            return response, 500

        try:
            conn = sqlite3.connect('api.db')
            conn.execute("INSERT INTO NOTIFICATIONS(TITLE,DESCRIPTION,ISREAD,USERID) " +
                         "VALUES('{0}','{1}',FALSE,{2})".format(args['title'],args['description'],args['user_id']))
            notificationID = conn.execute('SELECT last_insert_rowid() FROM NOTIFICATIONS;')
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "add successful"
        response['response'] = {'notification_id':notificationID,'title':args['title'],'description':args['description'],
                                'is_read':0,'user_id':args[user_id]}
        return response, 200

class CurrentPlacementGetByHouse(Resource):
    def get(self,house_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": [], "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT * FROM PLACEMENTS JOIN HOUSES ON HOUSES.HOUSEID=PLACEMENTS.HOUSEID " +
                             "WHERE PLACEMENTS.HOUSEID={0} AND PLACEMENTS.PLACE=HOUSES.CURRENTTURN AND FUTURECODE=0;".format(house_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['placement_id'] = row[0]
            temp['user_id'] = row[1]
            temp['house_id'] = row[2]
            temp['future_code'] = row[3]
            temp['place'] = row[4]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not any notifications for user with id {0}".format(user_id)
            response['returncode'] = 400
            return response, 200
        response['message'] = "search successful"
        response['response'] = data[0]
        return response, 200

class MakeDraftPick(Resource):
    def options(self,user_id,chore_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
            return response

        return 200;

    def put(self,user_id,chore_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": {}, "message": "", "returncode": 200}

        try:
            conn = sqlite3.connect('api.db')
            house_id = conn.execute("SELECT HOUSEID FROM CHORES WHERE CHOREID={0}".format(chore_id)).fetchone()[0]
            #conn.execute("PRAGMA foreign_keys = ON;")
            [currentUser,currentPlace] = conn.execute("SELECT PLACEMENTS.USERID,PLACEMENTS.PLACE FROM PLACEMENTS JOIN HOUSES ON HOUSES.HOUSEID=PLACEMENTS.HOUSEID " +
                             "WHERE PLACEMENTS.HOUSEID={0} AND PLACEMENTS.PLACE=HOUSES.CURRENTTURN AND FUTURECODE=0;".format(house_id)).fetchone()
            if(currentUser != user_id):
                response['message'] = "This user is not allowed to pick a chore yet"
                response['returncode'] = 400
                return response, 400
            conn.execute("UPDATE CHORES SET CLAIMED=TRUE, OWNERID={0} WHERE CHOREID={1};".format(user_id,chore_id))
            numChoresLeft = conn.execute("SELECT COUNT(*) FROM CHORES WHERE HOUSEID={0} AND CLAIMED=FALSE;".format(house_id)).fetchone()[0]
            if(numChoresLeft > 0):
                userCount = conn.execute("SELECT COUNT(*) FROM USERSTOHOUSES WHERE HOUSEID={0};".format(house_id)).fetchone()[0]
                nextPlace = (currentPlace + 1)%userCount
                conn.execute("UPDATE HOUSES SET CURRENTTURN={0} WHERE HOUSEID={1}".format(nextPlace,house_id))
                nextUser = conn.execute("SELECT USERID FROM PLACEMENTS WHERE HOUSEID={0} AND PLACE={1} AND FUTURECODE=0;".format(house_id,nextPlace)).fetchone()[0]
                conn.execute("INSERT INTO NOTIFICATIONS(TITLE,DESCRIPTION,ISREAD,USERID) " +
                    "VALUES('Your Pick','You are up to pick a chore',FALSE,{0});".format(nextUser))
            else:
                conn.execute("UPDATE HOUSES SET CURRENTPHASE='C' WHERE HOUSEID={0};".format(house_id))

                #move to own function, end draft logic
                placements = conn.execute("SELECT * FROM PLACEMENTS WHERE HOUSEID={0}".format(house_id))
                count = conn.execute("SELECT COUNT(*) FROM USERSTOHOUSES WHERE HOUSEID={0}".format(house_id)).fetchone()[0]
                changes_obj = conn.execute("SELECT REVERTPLACEMENTS.REVERTTO,REVERTPLACEMENTS.PLACEMENTID FROM REVERTPLACEMENTS JOIN PLACEMENTS ON REVERTPLACEMENTS.PLACEMENTID=PLACEMENTS.PLACEMENTID " +
                                       "WHERE PLACEMENTS.HOUSEID={0}".format(house_id))
                changes = []
                for row in changes_obj:
                    temp = {}
                    temp['revert_to'] = row[0]
                    temp['placement_id'] = row[1]
                    changes.append(temp)
                
                placement_org = []
                for row in placements:
                    temp = {}
                    if (row[0] in [x['placement_id'] for x in changes]) and (row[3] == 0):
                        revert = [x['revert_to'] for x in changes if x['placement_id'] == row[0]][0] 
                        temp['placement_id'] = row[0]
                        temp['user_id'] = revert
                        temp['house_id'] = row[2]
                        temp['future_code'] = (int(row[3])-1)%count
                        temp['place'] = row[4]
                        print(temp);
                        conn.execute("DELETE FROM REVERTPLACEMENTS WHERE PLACEMENTID={0}".format(row[0]))
                        placement_org.append(temp)
                    else:
                        temp['placement_id'] = row[0]
                        temp['user_id'] = row[1]
                        temp['house_id'] = row[2]
                        temp['future_code'] = (int(row[3])-1)%count
                        temp['place'] = row[4]
                        placement_org.append(temp)
                    
                    if row[3] == 0:
                        s = conn.execute("SELECT OFFERID FROM OFFEREDPLACEMENTS WHERE PLACEMENTID={0}".format(row[0]))
                        for row in s:
                            conn.execute("DELETE FROM OFFEREDCHORES WHERE OFFERID={0}".format(row[0]))
                            conn.execute("DELETE FROM OFFEREDPLACEMENTS WHERE OFFERID={0}".format(row[0]))
                            conn.execute("DELETE FROM OFFERS WHERE OFFERID={0}".format(row[0]))

                conn.execute("DELETE FROM PLACEMENTS WHERE HOUSEID={0}".format(house_id))
                for p in placement_org:
                    conn.execute("INSERT INTO PLACEMENTS(PLACEMENTID,USERID,HOUSEID,FUTURECODE,PLACE) VALUES({0},{1},{2},{3},{4})".format(p['placement_id'],p['user_id'],p['house_id'],p['future_code'],p['place']))
                
            
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            traceback.print_exc()
            response['returncode'] = 500
            return response, 500
        conn.commit()
        conn.close()
        response['message'] = "pick successful"
        return response, 200

class PlacementsGetByHouseAndUser(Resource):
    def get(self,house_id,user_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": [], "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute("SELECT * FROM PLACEMENTS WHERE HOUSEID={0} AND USERID={1}".format(house_id,user_id))
        except Exception as e:
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['placement_id'] = row[0]
            temp['user_id'] = row[1]
            temp['house_id'] = row[2]
            temp['future_code'] = row[3]
            temp['place'] = row[4]
            data.append(temp)
        conn.close()
        if len(data) < 1:
            response['message'] = "could not find any notifications for user with id {0}".format(user_id)
            response['returncode'] = 400
            return response, 200
        response['message'] = "search successful"
        response['response'] = data
        return response, 200

class OfferedPlacementsGetByOffer(Resource):
    def get(self,offer_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = {"response": [], "message": "", "returncode": 200}
        try:
            conn = sqlite3.connect('api.db')
            s = conn.execute(
                "SELECT * FROM OFFEREDPLACEMENTS " +
                "WHERE OFFERID={0};".format(offer_id))
        except Exception as e:
            traceback.print_exc()
            response['message'] = "Failed with the following error: {0}".format(e)
            response['returncode'] = 500
            return response, 500
        data = []
        for row in s:
            temp = {}
            temp['offer_id'] = row[0]
            temp['placement_id'] = row[1]
            temp['offer_side'] = row[2]
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
api.add_resource(NotificationsGetUnseenByUser, "/getunseennotificationsbyuser/<int:user_id>")
api.add_resource(OfferReject, "/rejectoffer/<int:offer_id>")
api.add_resource(NotificationsSetSeen, "/setseennotifications")
api.add_resource(NotificationAdd,"/addnotification")
api.add_resource(CurrentPlacementGetByHouse, "/getcurrentplacementbyhouse/<int:house_id>")
api.add_resource(MakeDraftPick, "/makedraftpick/<int:user_id>/<int:chore_id>")
api.add_resource(PlacementsGetByHouseAndUser, "/getplacementsbyhouseanduser/<int:house_id>/<int:user_id>")
api.add_resource(OfferedPlacementsGetByOffer, "/getofferedplacementsbyoffer/<int:offer_id>")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')