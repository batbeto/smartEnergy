import code
import influxdb

HOST = 'localhost'
PORT = 8086

class DBClient:
    """
    """
    def __init__(self, host=HOST, port=PORT):
        """
        """
        self.connect(host, port)

    def connect(self, host=HOST, port=PORT):
        """
        """
        self.client = influxdb.InfluxDBClient(host, port)

    def get_database_names(self):
        """
        """
        return self.client.get_list_database()

    def dump_database(self, dbname):
        """
        """
        query = 'SELECT * FROM "' + dbname + '"'
        self.client.switch_database(dbname)
        return self.client.query(query, epoch="s").get_points(measurement=dbname)

    def get_table(self, dbname):
        """
        """
        result = self.dump_database(dbname)
        ans = []
        for entry in result:
            line = []
            for field in code.FIELD:
                line.append(entry[field])
            ans.append(line)
        return ans
if __name__ == "__main__":

    c = DBClient()
    print(c.get_database_names())
    print(c.get_table(c.get_database_names()[-1]['name']))
