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
                        help='takes date')
    parser.add_argument('-s', '--state', type=str,
                        help='takes state')
    parser.add_argument('-p', '--place', type=str,
                        help='take name of any state or district or city(only use for --options demography)')
    parser.add_argument('-H', '--head', type=int,
                        help='process top rows by given number')
    parser.add_argument('-T', '--tail', type=int,
                        help='process last rows by given number')
    parser.add_argument('-D', '--daily', type=str,
                        help='if y(yes) daily count will be shown')
    parser.add_argument('-r', '--rank', type=int,
                        help='top rows will be shown by given value(donot use -r for graph type "whole")')
    parser.add_argument('--save', type=str,
                        help='save as csv to given path')
    parser.add_argument('-g', '--graph', type=str,
                        help='shows different types graph', choices=['whole', 'head', 'tail'])
    parser.add_argument('-f', '--of', type=str,
                        help='process data for selected type', choices=['Total_Confirmed', 'Total_Death',
                                                                        'Total_Recovered'])
    parser.add_argument('--options', type=str, required=True,
                        help='operations user want to do', choices=['show_data', 'demography',
                                                                    'state_dataset', 'data_by_date',
                                                                    'count_by_date', 'rank',
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
                        args.save+'show_data.csv', index=True)
                else:
                    print(init.show_data(of).head(args.head))
            elif args.tail != None:
                if args.save != None:
                    init.show_data(of).tail(args.tail).to_csv(
                        args.save+'show_data.csv', index=True)
                else:
                    print(init.show_data(of).tail(args.tail))
            elif args.head == None:
                if args.save != None:
                    init.show_data(of).to_csv(
                        args.save+'show_data.csv', index=True)
                else:
                    print(init.show_data(of))
            elif args.tail == None:
                if args.save != None:
                    init.show_data(of).to_csv(
                        args.save+'show_data.csv', index=True)
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
                df.head(args.head).to_csv(
                    args.save+f'demography_{args.place}_head_{args.head}.csv', index=True)
            else:
                print(df.head(args.head))
        elif args.tail != None:
            if args.save != None:
                df.tail(args.tail).to_csv(
                    args.save+f'demography_{args.place}_tail_{args.tail}.csv', index=True)
            else:
                print(df.tail(args.tail))
        elif args.head == None:
            if args.save != None:
                df.to_csv(args.save+f'demography_{args.place}.csv', index=True)
            else:
                print(df)
        elif args.tail == None:
            if args.save != None:
                df.to_csv(args.save+f'demography_{args.place}.csv', index=True)
            else:
                print(df)

    elif args.options == 'state_dataset':
        obj2 = Data(init)
        state = args.state
        df = obj2.get_dataset_state(state)
        if args.head != None:
            if args.save != None:
                df.head(args.head).to_csv(
                    args.save+f'{args.state}_head_{args.head}.csv')
            else:
                print(df.head(args.head))
        elif args.tail != None:
            if args.save != None:
                df.tail(args.tail).to_csv(
                    args.save+f'{args.state}_tail_{args.tail}.csv')
            else:
                print(df.tail(args.tail))
        elif args.head == None:
            if args.save != None:
                df.to_csv(args.save+f'{args.state}.csv')
            else:
                print(df)
        elif args.tail == None:
            if args.save != None:
                df.to_csv(args.save+f'{args.state}.csv')
            else:
                print(df)

    elif args.options == 'data_by_date':
        obj2 = Data(init)
        date = args.date
        df = obj2.get_dataset_by_date(date)
        if args.head != None:
            if args.save != None:
                df.head(args.head).to_csv(
                    args.save+f'{args.date.split("/")[0]}-{args.date.split("/")[1]}_head_{args.head}.csv')
            else:
                print(df.head(args.head))
        elif args.tail != None:
            if args.save != None:
                df.tail(args.tail).to_csv(
                    args.save+f'{args.date.split("/")[0]}-{args.date.split("/")[1]}_tail_{args.tail}.csv')
            else:
                print(df.tail(args.tail))
        elif args.head == None:
            if args.save != None:
                df.to_csv(
                    args.save+f'{args.date.split("/")[0]}-{args.date.split("/")[1]}.csv')
            else:
                print(df)
        elif args.tail == None:
            if args.save != None:
                df.to_csv(
                    args.save+f'{args.date.split("/")[0]}-{args.date.split("/")[1]}.csv')
            else:
                print(df)

    elif args.options == 'count_by_date':
        obj2 = Data(init)
        date = args.date
        by = args.of
        df = obj2.get_count_by_date(by.split('_')[1], date)
        if args.head != None:
            if args.save != None:
                df.head(args.head).to_csv(
                    args.save+f'count_by_{by.split("_")[1]}_{args.date.split("/")[0]}-{args.date.split("/")[1]}_head_{args.head}.csv')
            else:
                print(df.head(args.head))
        elif args.tail != None:
            if args.save != None:
                df.tail(args.tail).to_csv(
                    args.save+f'count_by_{by.split("_")[1]}_{args.date.split("/")[0]}-{args.date.split("/")[1]}_tail_{args.tail}.csv')
            else:
                print(df.tail(args.tail))
        elif args.head == None:
            if args.save != None:
                df.to_csv(
                    args.save+f'count_by_{by.split("_")[1]}_{args.date.split("/")[0]}-{args.date.split("/")[1]}.csv')
            else:
                print(df)
        elif args.tail == None:
            if args.save != None:
                df.to_csv(
                    args.save+f'count_by_{by.split("_")[1]}_{args.date.split("/")[0]}-{args.date.split("/")[1]}.csv')
            else:
                print(df)
    elif args.options == 'rank':
        obj2 = Data(init)
        num = args.rank
        by = args.of.split('_')[0]+f' {args.of.split("_")[1]}'
        df = obj2.rank(num, by, cumulative=True)
        if args.save != None:
            df.to_csv(args.save+f'rank_{args.rank}_top.csv')
        else:
            print(df)

    elif args.options == 'graph':
        obj3 = visualizer(init)
        if args.graph == 'whole':
            if args.rank == None:
                if args.state != None:
                    start = '30/1/2020'
                    end = datetime.strftime(datetime.strptime(
                        confirmed.columns[-1], '%m/%d/%Y'), '%d/%m/%Y')
                    if args.daily == 'y':

                        obj3.graph_by_date(
                            startDate=start, endDate=end, state=args.state, daily=True)
                    else:
                        obj3.graph_by_date(
                            startDate=start, endDate=end, state=args.state)
                else:
                    if args.daily == 'y':
                        obj3.whole(daily=True)
                    else:
                        obj3.whole()
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
                        obj3.graph_by_date(
                            startDate=s, endDate=e, state=args.state, daily=True)
                    else:
                        obj3.graph_by_date(
                            startDate=s, endDate=e, state=args.state)
                else:
                    if args.daily == 'y':
                        obj3.head(num=args.rank, daily=True)
                    else:
                        obj3.head(num=args.rank)
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
                        obj3.graph_by_date(
                            startDate=s, endDate=e, state=args.state, daily=True)
                    else:
                        obj3.graph_by_date(
                            startDate=s, endDate=e, state=args.state)
                else:
                    if args.daily == 'y':
                        obj3.tail(num=args.rank, daily=True)
                    else:
                        obj3.tail(num=args.rank)
            else:
                print('-r flag is required for tail type graph')


if __name__ == '__main__':
    main()
