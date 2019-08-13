import db
import code
import re
import sys



USAGE = """\
USAGE: code.py <filter> <field> <database-file>

  <filter>  date based filter
  <field>   time, FPA, FPB, FPC, P1, P2, P3, Q1, Q2, Q3

  Ex: 2018-01-01T15:35:00 2018-12-31T02:45:00 0-6 <database-file>
  weekdays= 0-monday, etc.
"""

if __name__ == "__main__":
    try:
        expr = ' '.join(sys.argv[1:-2])
        s_date = sys.argv[1]
        e_date = sys.argv[2]
        week_expr = "[" + sys.argv[3] + "]"
        week_pattern = re.compile(week_expr)
        dbpath = sys.argv[-1]
        table, content = code.read_data(dbpath)
    except:
        print(USAGE)
        sys.exit(0)

    """
    compare the table read from file to the table read from database (OK!)
    """
    #table_query = db.DBClient().get_table("Data_SensorsV2")
    #print(table == table_query)

    """
    iterate over the database and filter by datetime interval, later filter by
    weekday
    """
    
    s = code.timestamp_from_datetime(s_date)
    #print(s_date, s)
    e = code.timestamp_from_datetime(e_date)
    #print(e_date, e)
    s_hour = code.timestamp_from_time(s_date)
    #print(s_hour)
    e_hour = code.timestamp_from_time(e_date)
    #print(e_hour)
    
    intervaldb,errors = code.find_between_timestamps(table, s, e)

    # filter by weekday
    ans, ansH = code.filter_table(intervaldb, week_expr, week_pattern, s_hour, e_hour)
    #print(len(ans), len(ansH))
    
    code.write_csv(ansH)
    