import db
import code
import re
import sys
import datetime as dt


USAGE = """\
USAGE: code.py <filter> <field> <database-file>

  <filter>  date based filter
  <field>   time, FPA, FPB, FPC, P1, P2, P3, Q1, Q2, Q3

  Ex: 2018-01-01T15:35:00 2018-12-31T02:45:00 2018-11-29T20:45:00 0-6 P1 <database-file>
  weekdays= 0-monday, etc.
"""

if __name__ == "__main__":
    try:
        expr = ' '.join(sys.argv[1:-2])
        s_date = sys.argv[1]
        e_date = sys.argv[2]
        week_expr = "[" + sys.argv[4] + "]"
        week_pattern = re.compile(week_expr)
        d_date = sys.argv[3]
        field = sys.argv[-2]
        field_number = code.return_field(field)
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
    
    intervaldb,errors = code.find_between_timestamps(table, s, e)

    # filter by weekday
    ans, ansH = code.filter_table(intervaldb, week_expr, week_pattern, s_hour, e_hour)
    
    if errors != None:
        code.related_errors(errors)
    

    h_analyze = dt.datetime( int(d_date.split("-")[0]), int(d_date.split("-")[1]), int(d_date.split("-")[2][:2]) )
    #print(h_analyze)
    ###COMP_DATE -28 DAYS TO THE D_DATE (2419200 = 28 days)
    comp_date = h_analyze
    comp_date = h_analyze - dt.timedelta( days=28 )

    day_1 = []
    new_date = 0
    while new_date <= code.timestamp_from_datetime( e_date ):
        new_date = dt.datetime.timestamp(h_analyze)
        new_date_str = str( h_analyze ).split()
        new_date_str = 'T'.join(new_date_str)
        new_comp_date = dt.datetime.timestamp(comp_date)
        #gets a list of every data 28 days ago since the "present day"
        ans_28days = code.db_28days(table, new_comp_date, new_date)

        #gets a list completed by 0's ( disposable ), end precision that we got
        historic_efficience = code.efficience_table(ans_28days, week_expr,week_pattern)  

        #Get arithimetic mean to the present day and precision of data that we got
        mean_day, efficience_day, stdDev_mean, ans_day = code.mean_day(table,new_date_str,field_number) 

        #Gets the arithimetic mean of historic data
        historic_mean, historic_stdDev = code.db_mean( ans_28days, field_number )
        
        #Is a list of [ historic media, efficience of historic media, day media, efficience of day media ]
        day_1 += [[historic_mean, historic_efficience, historic_stdDev, mean_day, efficience_day, stdDev_mean]]

        h_analyze += dt.timedelta(days=1)
        comp_date = h_analyze - dt.timedelta(days=28)
    
    with open("plots/2018-05-12.csv", 'w') as file:
        for entry in day_1:
            file.write(str( entry )[1:-1]+'\n')
        file.close()

    standard_deviation_day = code.db_standard_deviation(ans_day ,field_number)

    standard_deviation_historic = code.db_standard_deviation(ans_28days, field_number)
    
    alarm_test = code.alarm_standard_deviation(mean_day, historic_mean, standard_deviation_day, standard_deviation_historic)
    
    #print(f"MD: {mean_day} HM: {historic_mean} SDD:{standard_deviation_day} SDH:{standard_deviation_historic}")
    
    '''
    with open( "28days.csv", 'w' ) as file:
        for entry in ans_28days_octave:
            file.write( str(entry)[1:-1]+"\n" )
        file.close()
    '''

    with open("day_alarm.csv", "w") as file_SmartEnergy:
        for entry in ans_day:
            
            file_SmartEnergy.write(str(entry)+" "+str(alarm_test)+"\n")
            
        file_SmartEnergy.close()
"""
    code.plot( ans_to_octave, s_date[:10], field )

    
    

    with open('2018_2019_filtro_Hora.txt', 'w+') as file_SmartEnergy:
        for i in ansH:
            file_SmartEnergy.write(str(i)+'\n')
        file_SmartEnergy.close()
        """