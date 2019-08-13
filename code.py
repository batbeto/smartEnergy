import datetime
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
    """ read the date from database
    """
    table = []
    content = open(filename).read().split()[1:]
    for line in content:
        line = line.split(',')[1:]
        table.append([float(i) for i in line])

    return table, content

def binary_search_day(day, table, start, end):
    """ doing a binary search in the database to be more fast
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
    """ looking for one day
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
    """ validate integer number in the date
    """
    try :
        year, month, day = [int(i) for i in date.split('-')]
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False

def weekday_from_timestamp(timestamp):
    """ return the weekday 
    """
    return datetime.datetime.fromtimestamp(timestamp).weekday()


def datetime_from_timestamp(timestamp):
    """convert timestamp to datetime
    """
    return datetime.date.fromtimestamp(timestamp)

def timestamp_from_datetime(date):
    """ convert datetime to timestamp
    """
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timestamp()

def timestamp_from_time(time):
    """return only the time from datetime
    """
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S").time()



def group_entries_by_day(table):
    """ doing a grupo of entries by day
    """
    ans = {}
    for entry in table:
        d = datetime_from_timestamp(entry[0])
        if d not in ans.keys():
            ans[d] = []
        ans[d].append(entry)
    return ans

def time_from_timestamp(timestamp):
    """ return only the time of timestamp
    """
    return datetime.datetime.fromtimestamp(timestamp).time()


def filter_table(intervaldb, week_expr, week_pattern, s_hour, e_hour):
    """filter of intervaldb to return date and hour
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

def write_csv(ansH):
    with open("dump_data.csv", 'w') as file:
        for entry in ansH:
            file.write(str( entry )+'\n')
        file.close()