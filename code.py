import datetime
from statistics import median
import numpy as np
from os import system


FIELD = {"time": 0,
         "FPA": 1,
         "FPB": 2,
         "FPC": 3,
         "P1": 4,
         "P2": 5,
         "P3": 6,
         "Q1": 7,
         "Q2": 8,
         "Q3": 9}

DAYS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", \
        "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24", \
        "25", "26", "27", "28", "29", "30", "31"]

WEEKDAYS = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]

def read_data(filename):
    """
    """
    table = []
    content = open(filename).read().split()[1:]
    for line in content:
        line = line.split(',')[1:]
        table.append([float(i) for i in line])

    return table, content

def binary_search_day(day, table, start, end):
    """
    """
    if start <= end:
        m = int((start + end) / 2)
        entry_day = datetime_from_timestamp(table[m][0])
        if day == entry_day:
            while (entry_day == day and m > 0):
                m = m - 1
                entry_day = datetime_from_timestamp(table[m][0])
            if day != entry_day:
                m = m + 1
            ans = []
            entry_day = datetime_from_timestamp(table[m][0])
            while day == entry_day:
                ans.append(table[m])
                m = m + 1
                entry_day = datetime_from_timestamp(table[m][0])
            return ans
        o_day = datetime.date.fromisoformat(day).toordinal()
        o_entry_day = datetime.date.fromisoformat(entry_day).toordinal()
        if o_day > o_entry_day:
            return binary_search_day(day, table, m + 1, end)
        else:
            return binary_search_day(day, table, start, m - 1)

def find_day(day, table):
    """
    """
    return binary_search_day(day, table, 0, len(table) - 1)

def find_between_timestamps(table, start, end):
    """ Find the interval in BD between passed parameters and try to find any discontinuity
    """

    aux = 0.0
    db_jump = []
    ans = []
    cont = 0
    for entry in table:
        if start <= entry[0] and end >= entry[0]:
            ans.append(entry)
        if (entry[0] - aux) >= 3660.0 and aux != 0.0:
            db_jump.append([aux,entry[0]])
            cont += 1
        aux = entry[0]    
    return ans, db_jump

def is_date_valid(date):
    """
    """
    try :
        year, month, day = [int(i) for i in date.split('-')]
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False

def weekday_from_timestamp(timestamp):
    """
    """
    return datetime.datetime.fromtimestamp(timestamp).weekday()

def month_from_timestamp(timestamp):
    """
    """
    return datetime.datetime.fromtimestamp(timestamp).month
def year_from_timestamp(timestamp):
    """
    """
    return datetime.datetime.fromtimestamp(timestamp).year

def datetime_from_timestamp(timestamp):
    """
    """
    return datetime.date.fromtimestamp(timestamp)

def timestamp_from_datetime(date):
    """
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timestamp()

def timestamp_from_time(time):
    """
    """
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S").time()

def group_entries_by_day(table):
    """
    """
    ans = {}
    for entry in table:
        d = datetime_from_timestamp(entry[0])
        if d not in ans.keys():
            ans[d] = []
        ans[d].append(entry)
    return ans


def time_from_timestamp(timestamp):
    """
    """
    return datetime.datetime.fromtimestamp(timestamp).time()

def related_errors(errors):
    """
    """
    with open('relatedErrors.txt', 'w') as file_SmartEnergy:
        for entry in errors:
            file_SmartEnergy.write(str(f'{time_from_timestamp(entry[0])} {datetime_from_timestamp(entry[0])} {entry[0]} '))
            file_SmartEnergy.write(str(f'{time_from_timestamp(entry[1])} {datetime_from_timestamp(entry[1])} {entry[1]} \n'))
        file_SmartEnergy.close()

def db_media(analyzer,field):
    """
    """
    sum_media = []
    if field in FIELD and field != 'time':
        number = FIELD[field]
        for entry in analyzer:
            sum_media.append(entry[number])
    mean = np.mean(sum_media)
    return mean

def db_median(analyzer,field):
    """
    """
    median_list = []
    if field in FIELD and field != 'time':
        number = FIELD[field]
        for entry in analyzer:
            median_list.append(entry[number])
    return median(median_list)

def db_standard_deviation(analyzer, field):
    """
    """
    sum_analyzer = []
    if field in FIELD and field != 'time':
        number = FIELD[field]
        for entry in analyzer:
            sum_analyzer.append(entry[number])
    svariance = np.var(sum_analyzer)
    dp = np.sqrt(variance)
    return dp

def filter_table(intervaldb, week_expr, week_pattern, s_hour, e_hour):
    """
    """
    ans = []
    ansH = []
    for entry in intervaldb:
        if week_expr != None:
            if week_pattern.match(str(weekday_from_timestamp(entry[0]))):
                ans.append(entry)
                if s_hour <= time_from_timestamp(entry[0]) and e_hour <= time_from_timestamp(entry[0]):
                    ansH.append(entry)
    return ans, ansH

def bd_29days(table, comp_date, h_analyze):
    """
    """
    table_28days = []
    for entry in table:
        if entry[0] > comp_date and entry[0] < (h_analyze-86400):
            table_28days.append(entry)
    return table_28days




def plot( table, name, field ):
    """
    """
    arch_name = name + ".csv"  #gets the name for the archive
    with open( "plots/"+arch_name, 'w' ) as archive:    #create the archive
        for i in table:
            archive.write( str(i)[1:-1] + "\n" )      #save every line
        archive.close()     #close the archive
    system( "octave plots/oc_plot.m plots/"+arch_name+" "+field )  #calls the octave script



