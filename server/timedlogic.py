import sqlite3
import datetime

def resetChores(conn, house_id):
    conn.execute("UPDATE CHORES SET CLAIMED=FALSE WHERE HOUSEID={0};".format(house_id))
    conn.execute("UPDATE HOUSES SET CURRENTPHASE='D', CURRENTTURN=0 WHERE HOUSEID={0};".format(house_id))
    placements = conn.execute("SELECT * FROM PLACEMENTS WHERE HOUSEID={0} AND FUTURECODE=0 AND PLACE=0;".format(house_id))
    placements = placements.fetchone()
    conn.execute("INSERT INTO NOTIFICATIONS(TITLE,DESCRIPTION,ISREAD,USERID) " +
                "VALUES('Your Pick','You are up to pick a chore',FALSE,{0});".format(placements[1]))
    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect('api.db')
    resetChores(conn,1)

# conn = sqlite3.connect('apis.db')
# houses = conn.execute("SELECT * FROM HOUSES")
# for row in houses:
#     if row[3] == 'd':

#     elif row[3] == 'w':
#     elif row[3] == 'm':


