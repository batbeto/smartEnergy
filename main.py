import db
import code
import re
import sys




USAGE = """\
USAGE: code.py <filter> <field> <database-file>

  <filter>  date based filter
  <field>   time, FPA, FPB, FPC, P1, P2, P3, Q1, Q2, Q3

  Ex: 2018-05-12T15:35:00 2019-02-05T02:45:00 2019-02-04T20:45:00 0,3-4 P1 <database-file>
  weekdays= 0-monday, etc.
"""
#print(sys.argv)
if __name__ == "__main__":
    try:
        expr = ' '.join(sys.argv[1:-2])
        s_date = sys.argv[1]
        e_date = sys.argv[2]
        week_expr = "[" + sys.argv[4] + "]"
        week_pattern = re.compile(week_expr)
        d_date = sys.argv[3]
        field = sys.argv[-2]
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
    #print(s)
    e = code.timestamp_from_datetime(e_date)
    #print(e)
    s_hour = code.timestamp_from_time(s_date)
    #print(s_hour)
    e_hour = code.timestamp_from_time(e_date)
    #print(e_hour)
    h_analyze = code.timestamp_from_datetime(d_date)
    #print(h_analyze)
    comp_date = h_analyze - 2419200###COMP_DATE -28 DAYS TO THE D_DATE (2419200 = 28 days)
    intervaldb,errors = code.find_between_timestamps(table, s, e)

    # filter by weekday
    ans, ansH = code.filter_table(intervaldb, week_expr, week_pattern, s_hour, e_hour)
    
    if errors != None:
        code.related_errors(errors)
    

    ans_28days = code.bd_29days(ans, comp_date, h_analyze)
    
    with open( "28days.csv", 'w' ) as file:
        for i in ans_28days:
            file.write( str(code.datetime_from_timestamp(i[0]) )+"\n" )
        file.close()


    """
    with open("TESTFILE.csv", 'w') as file:
        last_entry = ans_28days[0][0]
        for entry in ans_28days[1:]:
            time = entry[0]
            if time - last_entry >= 61:
                while time >= last_entry:
                    file.write("0\n")
                    time -= 60
                file.write("0\n")
            else:
                file.write(str(entry)[1:-1]+"\n")
            last_entry = entry[0]
        file.close()


    code.plot( ans_to_octave, s_date[:10], field )

    
    

    with open('2018_2019_filtro_Hora.txt', 'w+') as file_SmartEnergy:
        for i in ansH:
            file_SmartEnergy.write(str(i)+'\n')
        file_SmartEnergy.close()
        """