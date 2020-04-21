# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:17:34 2020

@author: Dripta
"""

from .covidindia import *
import argparse
from datetime import datetime, timedelta


def main():
    parser = argparse.ArgumentParser(
        description='Process some output of Covid-19 data in india.')
    parser.add_argument('-d', '--date', type=str,
                        help='takes date.For date range use two dates separated by "-"')
    parser.add_argument('-s', '--state', type=str,
                        help='takes state.It takes only state code.Do not use it for demography options')
    parser.add_argument('-p', '--place', type=str,
                        help='take name of any state or district or city.This flag only be used in demography options')
    parser.add_argument('-H', '--head', type=int,
                        help='process top rows by given number')
    parser.add_argument('-T', '--tail', type=int,
                        help='process last rows by given number')
    parser.add_argument('-D', '--daily', type=str,
                        help='if y(yes) daily count will be shown')
    parser.add_argument('-r', '--rank', type=int,
                        help='top rows will be shown by given value(donot use -r for graph type "whole")')
    parser.add_argument('--save', type=str,
                        help='save as csv to given path with file name(e.g.D:\path\where\to\filename.csv')
    parser.add_argument('-g', '--graph', type=str,
                        help='shows different types graph', choices=['whole', 'head', 'tail'])
    parser.add_argument('-f', '--of', type=str,
                        help='process data for selected type', choices=['Total_Confirmed', 'Total_Death',
                                                                        'Total_Recovered'])
    parser.add_argument('--options', type=str, required=True,
                        help='operations user want to do', choices=['show_data', 'demography',
                                                                    'state_dataset', 'data_by_date',
                                                                    'count_by_date', 'rank', 'cumulative_between_date',
                                                                    'count_between_date',
                                                                    'graph'])

    args = parser.parse_args()
    init = initializer(silent=True)
    confirmed = init.show_data(of='Confirmed')
    if args.options == 'show_data':
        of = args.of
        if '_' in of:
            of = of.split('_')[1]
            if args.head != None:
                if args.save != None:
                    init.show_data(of).head(args.head).to_csv(
                        args.save, index=True)
                else:
                    print(init.show_data(of).head(args.head))
            elif args.tail != None:
                if args.save != None:
                    init.show_data(of).tail(args.tail).to_csv(
                        args.save, index=True)
                else:
                    print(init.show_data(of).tail(args.tail))
            elif args.head == None:
                if args.save != None:
                    init.show_data(of).to_csv(args.save, index=True)
                else:
                    print(init.show_data(of))
            elif args.tail == None:
                if args.save != None:
                    init.show_data(of).to_csv(args.save, index=True)
                else:
                    print(init.show_data(of))
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
        num = args.rank
        if args.of != None:
            by = args.of.split('_')[0]+f' {args.of.split("_")[1]}'
            if args.daily == 'y':
                if args.date != None:
                    df = obj2.rank(num, by, cumulative=False, date=args.date)
                else:
                    df = obj2.rank(num, by, cumulative=False)
            else:
                if args.date != None:
                    df = obj2.rank(num, by, cumulative=True, date=args.date)
                else:
                    df = obj2.rank(num, by, cumulative=True)

            if args.save != None:
                df.to_csv(args.save)
            else:
                print(df)
        else:
            raise Exception('Use -f flag for which you want to rank')

    elif args.options == 'graph':
        obj3 = visualizer(init)
        if args.graph == 'whole':
            if args.rank == None:
                if args.state != None:
                    start = '30/1/2020'
                    end = datetime.strftime(datetime.strptime(
                        confirmed.columns[-1], '%m/%d/%Y'), '%d/%m/%Y')
                    if args.daily == 'y':

                        obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                           title=f'Daily count graph for {obj3.code[args.state]}', daily=True)
                    else:
                        obj3.graph_by_date(startDate=start, endDate=end, state=args.state,
                                           title=f'Cumulative count graph for {obj3.code[args.state]}')
                else:
                    if args.daily == 'y':
                        obj3.whole(
                            daily=True, title=f'Daily graph for all dates')
                    else:
                        obj3.whole(title=f'Cumulative graph for all dates')
            else:
                print('Do not use -r flag for whole type of graph')

        elif args.graph == 'head':
            if args.rank != None:
                if args.state != None:
                    s = '30/01/2020'
                    e = datetime.strftime(datetime.strptime(
                        s, '%d/%m/%Y')+timedelta(args.rank), '%d/%m/%Y')
                    if args.daily == 'y':

                        # obj3.head(num=args.rank,daily=True)
                        obj3.graph_by_date(startDate=s, endDate=e, state=args.state, daily=True,
                                           title=f'Daily graph of 1st {args.rank} days of {obj3.code[args.state]}')
                    else:
                        obj3.graph_by_date(startDate=s, endDate=e, state=args.state,
                                           title=f'Cumulative graph of 1st {args.rank} days of {obj3.code[args.state]}')
                else:
                    if args.daily == 'y':
                        obj3.head(num=args.rank, daily=True,
                                  title=f'Daily graph of 1st {args.rank} days')
                    else:
                        obj3.head(
                            num=args.rank, title=f'Cumulative graph of 1st {args.rank} days')
            else:
                print('-r flag is required for head type graph')

        elif args.graph == 'tail':
            if args.rank != None:
                if args.state != None:
                    time = confirmed.columns[-1]
                    d = datetime.strptime(time, '%m/%d/%Y')
                    s = datetime.strftime(d-timedelta(args.rank), '%d/%m/%Y')
                    e = datetime.strftime(d, '%d/%m/%Y')
                    if args.daily == 'y':

                        # obj3.head(num=args.rank,daily=True)
                        obj3.graph_by_date(startDate=s, endDate=e, state=args.state, daily=True,
                                           title=f'Daily graph of last {args.rank} days of {obj3.code[args.state]}')
                    else:
                        obj3.graph_by_date(startDate=s, endDate=e, state=args.state,
                                           title=f'Cumulative graph of last {args.rank} days of {obj3.code[args.state]}')
                else:
                    if args.daily == 'y':
                        obj3.tail(num=args.rank, daily=True,
                                  title=f'Daily graph of last {args.rank} days')
                    else:
                        obj3.tail(
                            num=args.rank, title=f'Cumulative graph of last {args.rank} days')
            else:
                print('-r flag is required for tail type graph')

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
                        df.head(args.head).to_csv(
                            args.save)
                    else:
                        print(df.head(args.head))
                elif args.tail != None:
                    if args.save != None:
                        df.tail(args.tail).to_csv(
                            args.save)
                    else:
                        print(df.tail(args.tail))
                else:
                    if args.save != None:
                        df.to_csv(
                            args.save)
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
                        df.head(args.head).to_csv(
                            args.save)
                    else:
                        print(df.head(args.head))
                elif args.tail != None:
                    if args.save != None:
                        df.tail(args.tail).to_csv(
                            args.save)
                    else:
                        print(df.tail(args.tail))
                else:
                    if args.save != None:
                        df.to_csv(
                            args.save)
                    else:
                        print(df)
            else:
                print('Give to dates separated by "-" (eg. 05/02/2020-06/03/2020)')
        else:
            print('-f flag should be given')


if __name__ == '__main__':
    main()
