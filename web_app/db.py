import psycopg2

class DatabaseConnection:
    def __init__(self, dbname='bookstore', user='postgres',
                 password='password', host='localhost', port=5432):
        self.conn_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Connection established.")
        except Exception as e:
            print("Connection error:")
            print(str(e).encode('utf-8', 'replace'))
            self.conn = None

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
        if not self.conn:
            print("No active DB connection!")
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor

        except Exception as e:
            print("SQL error:")
            print("Query:", query)
            print("Params:", params)
            print(str(e).encode('utf-8', 'replace'))

            if self.conn:
                self.conn.rollback()

            return None
