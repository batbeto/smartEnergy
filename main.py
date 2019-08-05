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
    comp_date = h_analyze - 2592000###COMP_DATE -30 DAYS TO THE D_DATE (2592000 = 30 days)
    intervaldb,errors, year_analyzer = code.find_between_timestamps(table, s, e)

    # filter by weekday
    ans_30 = []
    ans = []
    ansH = []
    ans_to_octave = []
    cont = 0
    for entry in intervaldb:
        if week_expr != None:
            if week_pattern.match(str(code.weekday_from_timestamp(entry[0]))):
                ans.append(entry)
                ans_to_octave += [entry[:]]
                ans_to_octave[cont].append( float(code.weekday_from_timestamp(entry[0])))
                if s_hour <= code.time_from_timestamp(entry[0]) and e_hour <= code.time_from_timestamp(entry[0]):
                    ansH.append(entry)
                    #print(f'{code.time_from_timestamp(entry[0])} {code.datetime_from_timestamp(entry[0])} {entry}')
                    if entry[0] >= comp_date:
                        ans_30.append(entry)
                        #print(f'{code.time_from_timestamp(entry[0])} {code.datetime_from_timestamp(entry[0])} {entry}')
                cont += 1
    if errors != None:
        code.related_errors(errors)
    if year_analyzer != None:
        print(code.db_media(year_analyzer, field))
        print(code.db_median(year_analyzer, field))


    print(code.db_dp(ans_30,field))

    code.plot( ans_to_octave, s_date[:10], field )




    '''

    with open('2018_2019_filtro_Hora.txt', 'w+') as file_SmartEnergy:
        for i in ansH:
            file_SmartEnergy.write(str(i)+'\n')
        file_SmartEnergy.close()

'''




    # TODO filter by hour-minute-second interval


    # group data by day
    """
    ans = code.group_entries_by_day(ans)
    for group in ans:
        s = 0.0
        for entry in ans[group]:
            s = s + entry[code.FIELD[field]]
        print(group, s / len(ans[group]), len(ans[group]), len(ans[group]) / 1439.0)
    """
