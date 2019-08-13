def date_from_str(date):
    """return only the date from datetime
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").date()

def db_28days(table, comp_date, h_analyze):
    """creating a interval of 28 days
    """
    
    table_28days = []
    for entry in table:
        if date_from_timestamp(entry[0]) > comp_date and date_from_timestamp(entry[0]) < (h_analyze - datetime.timedelta(days = 1) ):         
            table_28days.append(entry)         
    return table_28days



def date_from_timestamp(timestamp):
    """
    """
    return datetime.datetime.fromtimestamp(timestamp).date()

def return_field(field):
    if field in FIELD:
        number = FIELD[field]
    return number

def efficience_table(table, week_expr, week_pattern):
    """calculating the efficience of the table!
    """
    TIME_ARG = {0:0,
                1:5760,
                2:11520,
                3:17280,
                4:23040,
                5:28800,
                6:34560,
                7:40320}
    number = -1
    for entry in TIME_ARG:
        if week_expr != None:
            if week_pattern.match(str(TIME_ARG[entry])):
                number += 1

    if (number in TIME_ARG and number != 0) and len(table) != 0: 
        efficient_tax = ( len(table) / TIME_ARG[number] ) * 100
    else:
        return -1
        
    return efficient_tax

def mean_day(table, h_analyze_date, field_number, s_hour, e_hour):
    """
    """
    mean_today_list = []
    for entry in table:
        if date_from_timestamp(entry[0]) == h_analyze_date:
            mean_today_list.append(entry)
    if len( mean_today_list ) > 0:
        mean_day, stdDev_day = db_mean(mean_today_list, field_number)
    else:
        mean_day = -1
        stdDev_day = -1

    return mean_day, efficience_to_day(s_hour, e_hour, mean_today_list), stdDev_day

def efficience_to_day(s_hour, e_hour, table):
    """1440
    """
    hour1 = str(s_hour).split(":")
    hour_1 = (int(hour1[0])*60)+int(hour1[1])
    hour2 = str(e_hour).split(":")
    hour_2 = (int(hour2[0])*60)+int(hour2[1])
    
    if hour_1 > hour_2:
        hour_1 = 1440 - hour_1 
        eficience_time = (hour_1+hour_2)
    elif hour_2 > hour_1:
        eficience_time = hour_2 - hour_1
    else:
        eficience_time = hour_2 - hour_1

    return ( len(table) / eficience_time )*100

def plot( table, name, field ):
    """plot maker!
    """
    arch_name = name + ".csv"  #gets the name for the archive
    with open( "plots/"+arch_name, 'w' ) as archive:    #create the archive
        for i in table:
            archive.write( str(i)[1:-1] + "\n" )      #save every line
        archive.close()     #close the archive
    system( "octave plots/oc_plot.m plots/"+arch_name+" "+field )  #calls the octave script

    def db_mean(analyzer,field_number):
        """ calculating mean 
        """
        sum_mean = []
        for entry in analyzer:
            sum_mean.append(entry[field_number])
        mean = np.mean(sum_mean)
        std_dev = np.std(sum_mean)
        return mean, std_dev
    
    def db_median(analyzer,field_number):
        """finding median
        """
        median_list = []
        for entry in analyzer:
            median_list.append(entry[field_number])
        return median(median_list)
    
def related_errors(errors):
    """archive the related errors of the database
    """
    with open('relatedErrors.txt', 'w') as file_SmartEnergy:
        for entry in errors:
            file_SmartEnergy.write(str(f'{time_from_timestamp(entry[0])} {datetime_from_timestamp(entry[0])} {entry[0]} '))
            file_SmartEnergy.write(str(f'{time_from_timestamp(entry[1])} {datetime_from_timestamp(entry[1])} {entry[1]} \n'))
        file_SmartEnergy.close()
        
        
        
        ###################     ISTO ERA DO MAIN    ###################
        comp_date = h_analyze_date - dt.timedelta( days=28 )
        '''
        print(comp_date)
        print(type(comp_date))  
        '''

        if errors != None:
            code.related_errors(errors)
        
        
    
        h_analyze = code.timestamp_from_datetime(d_date)
        h_analyze_date = code.date_from_timestamp(h_analyze)
    
        ###COMP_DATE -28 DAYS TO THE D_DATE (2419200 = 28 days)
    
    day_1 = []
    while h_analyze_date <= code.date_from_str( e_date ):
        
        
        #gets a list of every data 28 days ago since the "present day"
        ans_28days = code.db_28days(ansH, comp_date, h_analyze_date)

        #Precision that we got
        historic_efficience = code.efficience_table(ans_28days, week_expr,week_pattern)

        #Get arithimetic mean to the present day and precision of data that we got
        mean_day, efficience_day, stdDev_day = code.mean_day(ansH,h_analyze_date,field_number, s_hour, e_hour) 

        #Gets the arithimetic mean of historic data
        historic_mean, historic_stdDev = code.db_mean( ans_28days, field_number )
        
        #Is a list of [ historic media, efficience of historic media, standard deviation of historic data, day media, efficience of day media, standar deviation of the day ]
        day_1.append([historic_mean, historic_efficience, historic_stdDev, mean_day, efficience_day, stdDev_day])

        h_analyze_date += dt.timedelta(days=1)
        comp_date = h_analyze_date - dt.timedelta(days=28)



    

    
    
    
    
    #print(f"MD: {mean_day} HM: {historic_mean} SDD:{standard_deviation_day} SDH:{standard_deviation_historic}")
    
    '''
    with open( "28days.csv", 'w' ) as file:
        for entry in ans_28days_octave:
            file.write( str(entry)[1:-1]+"\n" )
        file.close()
    '''
"""
    code.plot( ans_to_octave, s_date[:10], field )

    
    

    with open('2018_2019_filtro_Hora.txt', 'w+') as file_SmartEnergy:
        for i in ansH:
            file_SmartEnergy.write(str(i)+'\n')
        file_SmartEnergy.close()
        """


