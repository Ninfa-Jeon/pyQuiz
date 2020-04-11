import sqlite3 as sql
try:
    conn=sql.connect('Questions.db')
    query='''SELECT * FROM scoreboard
    '''
    cur=conn.cursor()
    cur.execute(query)
    record = cur.fetchall()
    for rec in record:
        print(rec)
    conn.commit()
    cur.close()
except sql.Error as err:
    print("Error: ",err)
finally:
    if conn:
        conn.close()
        print("sql connection closed")
