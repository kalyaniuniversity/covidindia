# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:17:34 2020

@author: Dripta
"""

from .covidindia import *
import argparse
from datetime import datetime, timedelta

init = initializer(silent=True)
confirmed = init.show_data(of='Confirmed')


def main():
    parser = argparse.ArgumentParser(
        description='Process some output of Covid-19 data in india.')
    parser.add_argument('-d', '--date', type=str,
                        help='takes date.For date range use two dates separated by "-"')
    parser.add_argument('-s', '--state', type=str,
                        help='takes state.It takes only state code.If state name has two names separated by space use " " around the name.Do not use it for demography options')
    parser.add_argument('-p', '--place', type=str,
                        help='take name of any state or district or city.If place name has two names separated by space use " " around the name.This flag only be used in demography options')
    parser.add_argument('-H', '--head', type=int,
                        help='process top rows by given number')
    parser.add_argument('-T', '--tail', type=int,
                        help='process last rows by given number')
    parser.add_argument('-D', '--daily', type=str,
                        help='if y(yes) daily count will be shown')
    parser.add_argument('-r', '--rank', type=str, choices=['top', 'bottom'],
                        help='top/bottom data will be shown by given value(donot use -r for graph type "whole")')
    parser.add_argument('-n', '--number', type=int,
                        help='No of data points user want to see(donot use -n for graph type "whole")')
    parser.add_argument('--save', type=str,
                        help='save as csv to given path with file name(e.g.D:\path\where\to\filename.csv')
    parser.add_argument('-g', '--graph', type=str,
                        help='shows different types graph', choices=['whole', 'head', 'tail', 'graph_by_date'])
    parser.add_argument('-f', '--of', type=str,
                        help='process data for selected type', choices=['Total_Confirmed', 'Total_Death',
                                                                        'Total_Recovered'])
    parser.add_argument('--options', type=str,
                        help='operations user want to do', choices=['show_data', 'demography',
                                                                    'state_dataset', 'data_by_date',
                                                                    'count_by_date', 'rank', 'cumulative_between_date',
                                                                    'count_between_date',
                                                                    'graph', 'district_data', 'tested_data'])

    subparsers = parser.add_subparsers(
        help='sub-command for cov-server', dest="command")
    parser_a = subparsers.add_parser('cov-server', help='starts the server')
    parser_a.add_argument('-b', '--bind', type=str,
                          help='mention to bind port(e.g. -b :4000)')

    args = parser.parse_args()

    if args.command == 'cov-server':
        from .SERVER.server import covserver
        serv = covserver()
        if args.bind != None:
            port = int(args.bind.split(':')[1])
            serv.run(port=port)
        elif args.bind == None:
            serv.run(port=5000)

    elif args.options != None:

        if args.options == 'show_data':
            of = args.of
            if '_' in of:
                of = of.split('_')[1]
                if args.daily != None:
                    _daily = True
                else:
                    _daily = False
                if args.head != None:
                    if args.save != None:
                        init.show_data(of, _daily).head(args.head).to_csv(
                            args.save, index=True)
                    else:
                        print(init.show_data(of, _daily).head(args.head))
                elif args.tail != None:
                    if args.save != None:
                        init.show_data(of, _daily).tail(args.tail).to_csv(
                            args.save, index=True)
                    else:
                        print(init.show_data(of, _daily).tail(args.tail))
                elif args.head == None:
                    if args.save != None:
                        init.show_data(of, _daily).to_csv(
                            args.save, index=True)
                    else:
                        print(init.show_data(of, _daily))
                elif args.tail == None:
                    if args.save != None:
                        init.show_data(of, _daily).to_csv(
                            args.save, index=True)
                    else:
                        print(init.show_data(of, _daily))
            else:
                print('Invalid Choice')

        elif args.options == 'demography':
            demo = Demographic_overview(init, silent=True)
            try:
                df = demo.demography(place=args.state, date=args.date)
            except:
                df = demo.demography(place=args.place, date=args.date)
            if args.head != None:
                if args.save != None:
                    df.head(args.head).to_csv(args.save, index=True)
                else:
                    print(df.head(args.head))
            elif args.tail != None:
                if args.save != None:
                    df.tail(args.tail).to_csv(args.save, index=True)
                else:
                    print(df.tail(args.tail))
            elif args.head == None:
                if args.save != None:
                    df.to_csv(args.save, index=True)
                else:
                    print(df)
            elif args.tail == None:
                if args.save != None:
                    df.to_csv(args.save, index=True)
                else:
                    print(df)

        elif args.options == 'state_dataset':
            obj2 = Data(init)
            state = args.state
            if args.daily == 'y':
                if args.state != None:
                    df = obj2.get_dataset_state(args.state, daily=True)
                elif args.of == None:
                    raise Exception(
                        'Please specify -f flag for which you want to see daily count data for all states')
                else:
                    df = obj2.get_dataset_state(
                        daily=True)[f'{args.of.split("_")[1]}']
            else:
                if args.state != None:
                    df = obj2.get_dataset_state(args.state)
                else:
                    df = obj2.get_dataset_state()
            if args.head != None:
                if args.save != None:
                    df.head(args.head).to_csv(args.save)
                else:
                    print(df.head(args.head))
            elif args.tail != None:
                if args.save != None:
                    df.tail(args.tail).to_csv(args.save)
                else:
                    print(df.tail(args.tail))
            elif args.head == None:
                if args.save != None:
                    df.to_csv(args.save)
                else:
                    print(df)
            elif args.tail == None:
                if args.save != None:
                    df.to_csv(args.save)
                else:
                    print(df)

        elif args.options == 'data_by_date':
            obj2 = Data(init)
            date = args.date
            df = obj2.get_dataset_by_date(date)
            if args.head != None:
                if args.save != None:
                    df.head(args.head).to_csv(args.save)
                else:
                    print(df.head(args.head))
            elif args.tail != None:
                if args.save != None:
                    df.tail(args.tail).to_csv(args.save)
                else:
                    print(df.tail(args.tail))
            elif args.head == None:
                if args.save != None:
                    df.to_csv(args.save)
                else:
                    print(df)
            elif args.tail == None:
                if args.save != None:
                    df.to_csv(args.save)
                else:
                    print(df)

        elif args.options == 'count_by_date':
            obj2 = Data(init)
            date = args.date
            by = args.of
            df = obj2.get_count_by_date(by.split('_')[1], date)
            if args.head != None:
                if args.save != None:
                    df.head(args.head).to_csv(args.save)
                else:
                    print(df.head(args.head))
            elif args.tail != None:
                if args.save != None:
                    df.tail(args.tail).to_csv(args.save)
                else:
                    print(df.tail(args.tail))
            elif args.head == None:
                if args.save != None:
                    df.to_csv(args.save)
                else:
                    print(df)
            elif args.tail == None:
                if args.save != None:
                    df.to_csv(args.save)
                else:
                    print(df)
        elif args.options == 'rank':
            obj2 = Data(init)
            num = args.number
            if args.rank != None:
                if args.of != None:
                    by = args.of.split('_')[0]+f' {args.of.split("_")[1]}'
                    if args.daily == 'y':
                        if args.date != None:
                            df = obj2.rank(num, by, kind=args.rank,
                                           cumulative=False, date=args.date)
                        else:
                            df = obj2.rank(
                                num, by, kind=args.rank, cumulative=False)
                    else:
                        if args.date != None:
                            df = obj2.rank(num, by, kind=args.rank,
                                           cumulative=True, date=args.date)
                        else:
                            df = obj2.rank(
                                num, by, kind=args.rank, cumulative=True)

                    if args.save != None:
                        df.to_csv(args.save)
                    else:
                        print(df)
                else:
                    raise Exception('Use -f flag for which you want to rank')
            else:
                raise Exception('Please specify the -r flag')

        elif args.options == 'graph':
            obj3 = visualizer(init)
            if args.graph == 'whole':
                if args.number == None:
                    if args.state != None:
                        start = '30/1/2020'
                        end = datetime.strftime(datetime.strptime(
                            confirmed.columns[-1], '%m/%d/%Y'), '%d/%m/%Y')
                        if args.daily == 'y':
                            if args.of != None:
                                obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                   title=f'{args.of.split("_")[1].lower()} Daily count graph for {obj3.code[args.state]}', daily=True, typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                   title=f'Daily count graph for {obj3.code[args.state]}', daily=True)
                        else:
                            if args.of != None:
                                obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                   title=f'{args.of.split("_")[1].lower()} Cumulative count graph for {obj3.code[args.state]}', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                   title=f'Cumulative count graph for {obj3.code[args.state]}')
                    else:
                        if args.daily == 'y':
                            if args.of != None:
                                obj3.whole(
                                    daily=True, title=f'{args.of.split("_")[1].lower()} Daily graph for all dates', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.whole(
                                    daily=True, title=f'Daily graph for all dates')
                        else:
                            if args.of != None:
                                obj3.whole(title=f'{args.of.split("_")[1].lower()} Cumulative graph for all dates', typeof=args.of.split(
                                    '_')[1].lower())
                            else:
                                obj3.whole(
                                    title=f'Cumulative graph for all dates')
                else:
                    print('Do not use -n flag for whole type of graph')

            elif args.graph == 'head':
                if args.number != None:
                    if args.state != None:
                        s = '30/01/2020'
                        e = datetime.strftime(datetime.strptime(
                            s, '%d/%m/%Y')+timedelta(args.number), '%d/%m/%Y')
                        if args.daily == 'y':
                            if args.of != None:
                                # obj3.head(num=args.rank,daily=True)
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state, daily=True,
                                                   title=f'{args.of.split("_")[1].lower()} Daily graph of 1st {args.number} days of {obj3.code[args.state]}', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state, daily=True,
                                                   title=f'Daily graph of 1st {args.number} days of {obj3.code[args.state]}')
                        else:
                            if args.of != None:
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state,
                                                   title=f'{args.of.split("_")[1].lower()} Cumulative graph of 1st {args.number} days of {obj3.code[args.state]}', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state,
                                                   title=f'Cumulative graph of 1st {args.number} days of {obj3.code[args.state]}')
                    else:
                        if args.daily == 'y':
                            if args.of != None:
                                obj3.head(
                                    num=args.number, daily=True, title=f'{args.of.split("_")[1].lower()} Daily graph of 1st {args.number} days for all states', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.head(
                                    num=args.number, daily=True, title=f'Daily graph of 1st {args.number} days for all states')
                        else:
                            if args.of != None:
                                obj3.head(
                                    num=args.number, title=f'{args.of.split("_")[1].lower()} Cumulative graph of 1st {args.number} days for all states', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.head(
                                    num=args.number, title=f'Cumulative graph of 1st {args.number} days for all states')
                else:
                    print('-n flag is required for head type graph')

            elif args.graph == 'tail':
                if args.number != None:
                    if args.state != None:
                        time = confirmed.columns[-1]
                        d = datetime.strptime(time, '%m/%d/%Y')
                        s = datetime.strftime(
                            d-timedelta(args.number), '%d/%m/%Y')
                        e = datetime.strftime(d, '%d/%m/%Y')
                        if args.daily == 'y':
                            if args.of != None:
                                # obj3.head(num=args.rank,daily=True)
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state, daily=True,
                                                   title=f'{args.of.split("_")[1].lower()} Daily graph of last {args.number} days of {obj3.code[args.state]}', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state, daily=True,
                                                   title=f'Daily graph of last {args.number} days of {obj3.code[args.state]}')
                        else:
                            if args.of != None:
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state,
                                                   title=f'{args.of.split("_")[1].lower()} Cumulative graph of last {args.number} days of {obj3.code[args.state]}', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.graph_by_date(startDate=s, endDate=e, state=args.state,
                                                   title=f'Cumulative graph of last {args.number} days of {obj3.code[args.state]}')
                    else:
                        if args.daily == 'y':
                            if args.of != None:
                                obj3.tail(num=args.number, daily=True,
                                          title=f'{args.of.split("_")[1].lower()} Daily graph of last {args.number} days', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.tail(num=args.number, daily=True,
                                          title=f'Daily graph of last {args.number} days')
                        else:
                            if args.of != None:
                                obj3.tail(
                                    num=args.number, title=f'{args.of.split("_")[1].lower()} Cumulative graph of last {args.number} days', typeof=args.of.split('_')[1].lower())
                            else:
                                obj3.tail(
                                    num=args.number, title=f'Cumulative graph of last {args.number} days')
                else:
                    print('-n flag is required for tail type graph')

            elif args.graph == 'graph_by_date':
                if args.date != None:
                    if '-' in args.date:
                        start = args.date.split('-')[0]
                        end = args.date.split('-')[1]
                        if args.state != None:

                            if args.daily == 'y':
                                if args.of != None:
                                    obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                       title=f'{args.of.split("_")[1].lower()} Daily graph between {start} and {end} of {obj3.code[args.state]}',
                                                       daily=True, typeof=args.of.split('_')[1].lower())
                                else:
                                    obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                       title=f'Daily graph between {start} and {end} of {obj3.code[args.state]}',
                                                       daily=True)
                            else:
                                if args.of != None:
                                    obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                       title=f'{args.of.split("_")[1].lower()} Cumulative graph between {start} and {end} of {obj3.code[args.state]}',
                                                       daily=False, typeof=args.of.split('_')[1].lower())
                                else:
                                    obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                                       title=f'Cumulative graph between {start} and {end} of {obj3.code[args.state]}',
                                                       daily=False)
                        else:
                            if args.daily == 'y':
                                if args.of != None:
                                    obj3.graph_by_date(startDate=start, endDate=end,
                                                       title=f'{args.of.split("_")[1].lower()} Daily graph between {start} and {end} of all states',
                                                       daily=True, typeof=args.of.split('_')[1].lower())
                                else:
                                    obj3.graph_by_date(startDate=start, endDate=end,
                                                       title=f'Daily graph between {start} and {end} of all states',
                                                       daily=True)
                            else:
                                if args.of != None:
                                    obj3.graph_by_date(startDate=start, endDate=end,
                                                       title=f'Cumulative graph between {start} and {end} of all states',
                                                       daily=False, typeof=args.of.split('_')[1].lower())
                                else:
                                    obj3.graph_by_date(startDate=start, endDate=end,
                                                       title=f'{args.of.split("_")[1].lower()} Cumulative graph between {start} and {end} of all states',
                                                       daily=False)
                    else:
                        raise Exception('Two Dates must be separated by "-"')

        elif args.options == 'cumulative_between_date':
            obj2 = Data(init)
            if args.of != None:
                if '-' in args.date:
                    of = args.of.replace('_', " ")
                    date = args.date.split('-')
                    df = obj2.get_cum_dataset_between_date(
                        startDate=date[0], endDate=date[1], by=of)
                    if args.head != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    elif args.tail != None:
                        if args.save != None:
                            df.tail(args.tail).to_csv(args.save)
                        else:
                            print(df.tail(args.tail))
                    else:
                        if args.save != None:
                            df.to_csv(args.save)
                        else:
                            print(df)
                else:
                    print('Give to dates separated by "-" (eg. 05/02/2020-06/03/2020)')
            else:
                print('-f flag should be given')

        elif args.options == 'count_between_date':
            obj2 = Data(init)
            if args.of != None:
                if '-' in args.date:
                    of = args.of.split('_')[1]
                    date = args.date.split('-')
                    df = obj2.get_count_between_date(
                        startDate=date[0], endDate=date[1], by=of)
                    if args.head != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    elif args.tail != None:
                        if args.save != None:
                            df.tail(args.tail).to_csv(args.save)
                        else:
                            print(df.tail(args.tail))
                    else:
                        if args.save != None:
                            df.to_csv(args.save)
                        else:
                            print(df)
                else:
                    print('Give to dates separated by "-" (eg. 05/02/2020-06/03/2020)')
            else:
                print('-f flag should be given')

        elif args.options == 'district_data':
            obj2 = Data(init)
            if args.date != None:
                if args.daily != 'y':
                    df = obj2.get_district_data_by_date(
                        place=args.place, date=args.date)
                else:
                    df = obj2.get_district_data_by_date(
                        place=args.place, date=args.date, daily=True)
                if args.head != None:
                    if args.save != None:
                        df.head(args.head).to_csv(args.save)
                    else:
                        print(df.head(args.head))
                elif args.tail != None:
                    if args.save != None:
                        df.tail(args.tail).to_csv(args.save)
                    else:
                        print(df.tail(args.tail))
                else:
                    if args.save != None:
                        df.to_csv(args.save)
                    else:
                        print(df)
            else:
                if args.daily != 'y':
                    df = obj2.get_district_data_by_date(place=args.place)
                else:
                    df = obj2.get_district_data_by_date(
                        place=args.place, daily=True)
                if args.head != None:
                    if args.save != None:
                        df.head(args.head).to_csv(args.save)
                    else:
                        print(df.head(args.head))
                elif args.tail != None:
                    if args.save != None:
                        df.tail(args.tail).to_csv(args.save)
                    else:
                        print(df.tail(args.tail))
                else:
                    if args.save != None:
                        df.to_csv(args.save)
                    else:
                        print(df)

        elif args.options == 'tested_data':
            obj2 = Data(init)
            if args.state != None:
                if args.date != None:
                    df = obj2.tested_subject_data(
                        date=args.date, state=args.state)
                    if args.head != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    elif args.tail != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    else:
                        print(df)
                else:
                    df = obj2.tested_subject_data(state=args.state)
                    if args.head != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    elif args.tail != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    else:
                        print(df)
            else:
                if args.date != None:
                    df = obj2.tested_subject_data(date=args.date)
                    if args.head != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    elif args.tail != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    else:
                        print(df)
                else:
                    df = obj2.tested_subject_data()
                    if args.head != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    elif args.tail != None:
                        if args.save != None:
                            df.head(args.head).to_csv(args.save)
                        else:
                            print(df.head(args.head))
                    else:
                        print(df)

    else:
        raise Exception(
            '--options argument is required for non server functionalities')


if __name__ == '__main__':
    main()
