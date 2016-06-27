"""
Allocate Bowers cook cycle.
"""

import pandas as pd
import random
import argparse as ap
import datetime as py_dt
import numpy as np

# # Information about this cycle
# start_date = '6-6-2016'
# end_date = '6-24-2016'
# exclude_dates = ['6-8-2016', '6-22-2016']
# community_dinners = ['6-15-2016']
# fname = 'june_2016.csv'

# dir_name = 'data/'
# choice_cols = [u'Preferred day', u'Second choice', u'Third choice',
#                u'Fourth choice', u'Fifth choice']
# name_col = 'Your Name'

def format_date(s):
    month, day, year = s.split('-')
    if len(month) == 1:
        month = '0' + month
    return '-'.join([year, month, day])

def create_parser():
    parser = ap.ArgumentParser(description='generate an cook cycle assignment '
                               'based on n ranked preferences')
    parser.add_argument('start_date', help='date to start the cook cycle on '
                        '(inclusive)', type=str)
    parser.add_argument('end_date', help='date to end the cook cycle on '
                        '(inclusive)', type=str)
    parser.add_argument('preferences', help='path to list of date preferences, '
                        'dates should be in YYYY-MM-DD form, the file should '
                        'be a csv', type=str)
    parser.add_argument('-e', '--exclude_dates', help='list of dates to '
                        'exclude from cook cycle (YYYY-MM-DD format), must be '
                        'within start and end dates above', nargs='+', type=str)
    parser.add_argument('-c', '--community_dinners', help='list of dates on '
                        'which the house requires two cooks', nargs='+', 
                        type=str)
    parser.add_argument('-o', '--output', help='file to save schedule to'
                        '(default <start>_to_<end>_cookcycle.csv', type=str,
                        default='')
    return parser

def create_date_range(start, end, excl):
    range_ = pd.date_range(start, end)
    excl_range = range_[np.logical_not(range_.isin(excl))]
    excl_range = [str(d) for d in excl_range]
    return excl_range

def get_all_choices(data, all_dates):
    all_cho = all_dates
    other_cols = data.columns[2:]
    for c in other_cols:
        dl = data[c].tolist()
        dlf = []
        for d in dl:
            m, d, y = d.split('/')
            dlf.append(str(py_dt.datetime(int(y), int(m), int(d))))
        all_cho = all_cho + filter(lambda x: x in all_cho, dlf)
    choices = pd.Series(data=all_cho)
    return choices

def get_choice_date_order(data, all_dates, extr, n_extr=1):
    all_cho = get_all_choices(data, all_dates)
    sorted_cho = all_cho.value_counts(ascending=True)
    sorted_cho = sorted_cho.keys().tolist()
    sc_search = np.array(sorted_cho)
    for e in extr:
        y, m, d = e.split('-')
        dt = py_dt.datetime(int(y), int(m), int(d))
        da = str(dt)
        x = np.where(sc_search == da)[0][0]
        for i in xrange(n_extr):
            h = 24.*(i+1)/(n_extr + 1.)
            dta = py_dt.datetime(int(y), int(m), int(d), int(h))
            sorted_cho.insert(x, str(dta))
    return sorted_cho

def assign_dates(data, date_order):
    a = pd.DataFrame(columns=['name', 'date', 'choice'])
    unassigned = []
    for date in date_order:
        for cho in data.columns[2:]:
            choosers = data[data[cho] == date]
            if not choosers.empty:
                break
        if choosers.empty:
            unassigned.append(date)
        else:
            i_winner = random.choice(range(choosers.shape[0]))
            winner = choosers.iloc[i_winner]
            entry = {'name':winner[data.columns[1]],
                     'date':date,
                     'choice':cho}
            a = a.append(entry, ignore_index=True)
            data = data[data[data.columns[1]] != winner[data.columns[1]]]
    return a, unassigned

def assign_dates_continuous(data, date_order):
    a = pd.DataFrame(columns=['name','date','choice'])
    unassigned = []
    while len(date_order) > 0:
        date = date_order[0]
        y, m, d = date[:10].split('-')
        date = py_dt.datetime(int(y), int(m), int(d))
        date = '{}/{}/{}'.format(int(m), int(d), int(y))
        # date = date.date().strftime(u'%Y-%m-%d')
        for i, cho in enumerate(data.columns[2:]):
            choosers = data[data[cho] == date]
            if not choosers.empty:
                break
        if choosers.empty:
            unassigned.append(date)
        else:
            i_winner = random.choice(range(choosers.shape[0]))
            winner = choosers.iloc[i_winner]
            entry = {'name':winner[data.columns[1]],
                     'date':date,
                     'choice':cho,
                     'choice number':i+1}
            a = a.append(entry, ignore_index=True)
            data = data[data[data.columns[1]] != winner[data.columns[1]]]
        date_order = get_choice_date_order(data, date_order[1:], [])
    a = a.sort('date')
    return a, unassigned

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    
    data = pd.read_csv(args.preferences)
    date_range = create_date_range(args.start_date, args.end_date, 
                                   args.exclude_dates)
    date_order = get_choice_date_order(data, date_range, 
                                       args.community_dinners)
    print 'have {} dates for {} people'.format(len(date_order), len(data))
    assignments, unassigned = assign_dates_continuous(data, date_order)
    if len(args.output) == 0:
        fp = '{}_to_{}_cookcycle.csv'.format(args.start_date,
                                             args.end_date)
    else:
        fp = args.output
    assignments.to_csv(fp)
    print assignments
    print assignments['choice number'].mean()
    print 'unassigned', unassigned
