import config
import MySQLdb

class DB():
    def __init__(self):
        self.db = MySQLdb.connect(**config.db_config)    
    def query(self, sql_query):
        cur = self.db.cursor()
        cur.execute(sql_query)
        return cur

    def query_pretty(self, sql_query):
        cur = self.db.cursor()
        try:
            cur.execute(sql_query)
        except Exception as e:
            return str(e)
        output = ''
        
        numrows = cur.rowcount

        # Get and display one row at a time
        if numrows < 1:
            return 'Sorry! No result founds in our database!'
        for x in range(0, numrows):
            row = cur.fetchone()
            i = 0
            for i in range(len(cur.description)):
                output += '\n'
                output += str(cur.description[i][0])+ " --> "+ str(row[i])
            output += '\n'
            output += '-'*25
        return output

    def close(self):
        self.db.close()
