# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:24:51 2020

@author: Dripta

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import urllib
import json


class initializer():
    def __init__(self, silent=False):
        '''
        This is a class that will scrap the data from source upto the previous day of
        day of using that package.

        Returns
        -------
        None.

        '''
        if silent == False:
            print('Initializing.......')
            print('Scraping Raw data....')

        self.csv_Confirmed = pd.read_csv(
            "https://raw.githubusercontent.com/kalyaniuniversity/COVID-19-Datasets/master/India%20Statewise%20Confirmed%20Cases/COVID19_INDIA_STATEWISE_TIME_SERIES_CONFIRMED.csv")
        self.csv_recovered = pd.read_csv(
            'https://raw.githubusercontent.com/kalyaniuniversity/COVID-19-Datasets/master/India%20Statewise%20Recovery%20Cases/COVID19_INDIA_STATEWISE_TIME_SERIES_RECOVERY.csv')
        self.csv_Death = pd.read_csv(
            'https://raw.githubusercontent.com/kalyaniuniversity/COVID-19-Datasets/master/India%20Statewise%20Death%20Cases/COVID19_INDIA_STATEWISE_TIME_SERIES_DEATH.csv')
        column_dict = {i: j for j, i in enumerate(self.csv_Confirmed.columns)}
        self.code = pd.Series(list(
            self.csv_Confirmed['STATE/UT'][:-1]), index=list(self.csv_Confirmed['CODE'][:-1]))
        self.count_conf = pd.concat([self.csv_Confirmed['STATE/UT'], self.csv_Confirmed['1/30/2020'],
                                     self.csv_Confirmed.iloc[:, column_dict['1/30/2020']:].diff(axis=1).dropna(axis=1)], axis=1)
        self.count_recover = pd.concat([self.csv_recovered['STATE/UT'], self.csv_recovered['1/30/2020'],
                                        self.csv_recovered.iloc[:, column_dict['1/30/2020']:].diff(axis=1).dropna(axis=1)], axis=1)
        self.count_death = pd.concat([self.csv_Death['STATE/UT'], self.csv_Death['1/30/2020'],
                                      self.csv_Death.iloc[:, column_dict['1/30/2020']:].diff(axis=1).dropna(axis=1)], axis=1)
        if silent == False:
            print('All Scraping done \n converting in Dataframes')
            print('All setup done.')
            print('############################################################')
            print(f'\t\t\tOverview:-(upto {self.csv_Confirmed.columns[-1]})')
            print('Confirmed:', self.csv_Confirmed[self.csv_Confirmed.columns[-1]].tolist()[-1], '\tRecovered:',
                  self.csv_recovered[self.csv_recovered.columns[-1]].tolist()[-1], '\t\tDeceased:', self.csv_Death[self.csv_Death.columns[-1]].tolist()[-1])
            print('############################################################')

    # call this method to see all collected datasets
    # it returns a list of dataframes
    def show_data(self, of):
        '''
        This method only assembles the collected data 

        Returns
        -------
        list
            returns collected data as 3 dataframe format.

        '''
        if of.lower() == 'confirmed':
            return self.csv_Confirmed
        elif of.lower() == 'recovered':
            return self.csv_recovered
        elif of.lower() == 'death':
            return self.csv_Death


class Demographic_overview(initializer):
    def __init__(self, init, silent=False):
        '''
        This Demographic_overview class has the power of filtering in terms of state,
        district,city,date or range of date

        Returns
        -------
        None.

        '''
        if silent == False:
            print('Collecting Data.....')
        json_url = urllib.request.urlopen(
            'https://api.covid19india.org/raw_data.json')
        json_url_2 = urllib.request.urlopen(
            'https://api.covid19india.org/raw_data3.json')
        data_1 = json.loads(json_url.read())
        data_2 = json.loads(json_url_2.read())
        df_1 = pd.DataFrame(data_1['raw_data'])
        df_2 = pd.DataFrame(data_2['raw_data'])
        df = pd.concat([df_1, df_2])
        df = df.replace('', 'Unknown')
        df = df[(df['dateannounced'] != 'Unknown') & (
            df['dateannounced'] != datetime.strftime(datetime.now(), '%d/%m/%Y'))]
        index = []
        for i in df.dateannounced:
            if i != 'Unknown':
                index.append(datetime.strptime(i, '%d/%m/%Y'))
            else:
                index.append('Unknown')
        df.dateannounced = index
        self.raw = df
        self.code = init.code
        self.state = np.unique([i for i in self.raw['detectedstate']])
        self.district = np.unique([i for i in self.raw['detecteddistrict']])
        self.city = np.unique([i for i in self.raw['detectedcity']])
        if silent == False:
            print('All Done.')

    def demography(self, place='all', date='all'):
        '''
        This method can show the male and female count of confirmed cases for a state or a district or
        a city for a given date of range of date.        

        Parameters
        ----------
        place : character, optional
            place can be state or district or city.this method automatically recognize the place
            and gives user data for that place. The default is 'all'.If place is mentioned data for all places
            will be shown.
        date : character, optional
            by which date or range of date the data will be filtered.Date must be dd/mm/yyyy format.
            The default is 'all'.if date is not mentioned data for all dates will be shown

        Raises
        ------
        Exception
            If no data is found for a date or a place it will raise exceptions.

        Returns
        -------
        Dataframe
            dataframe consists of male female counts of confirmed cases for given date and place.

        '''
        # dateDict=dict(tuple(self.raw.groupby('dateannounced')))
        if place != 'all':
            if date != 'all':
                if '-' in date:
                    date = date.split('-')
                    date = [datetime.strptime(i, '%d/%m/%Y') for i in date]
                    try:
                        state = self.code[place]

                    except:
                        if 'and' in place.split(' '):
                            words = []
                            for i in place.split(" "):
                                if i != 'and':
                                    words.append(i.title())
                                else:
                                    words.append(i)
                            state = ' '.join(words)
                        else:
                            state = place.title()
                    if state in self.state:
                        state_filter = self.raw[self.raw['detectedstate'] == state]
                        date_filter = state_filter[(state_filter['dateannounced'] >= date[0]) & (
                            state_filter['dateannounced'] <= date[1])]
                        if date_filter.empty == False:
                            frame = pd.concat([date_filter['detecteddistrict'], date_filter['detectedcity'],
                                               date_filter['dateannounced'], date_filter['gender']], axis=1)
                            frame = frame.groupby(['detecteddistrict', 'detectedcity', 'dateannounced'])[
                                'gender'].value_counts()
                            return pd.DataFrame({'count': frame})
                        else:
                            raise Exception(
                                f'No Data found between {datetime.strftime(date[0],"%d/%m/%Y")} and {datetime.strftime(date[1],"%d/%m/%Y")}')
                    elif place.title() in self.district:
                        district_filter = self.raw[self.raw['detecteddistrict'] == place.title(
                        )]
                        date_filter = district_filter[(district_filter['dateannounced'] >= date[0]) & (
                            district_filter['dateannounced'] <= date[1])]
                        if date_filter.empty == False:
                            frame = pd.concat(
                                [date_filter['detectedcity'], date_filter['dateannounced'], date_filter['gender']], axis=1)
                            # print(frame)
                            frame = frame.groupby(['detectedcity', 'dateannounced'])[
                                'gender'].value_counts()
                            return pd.DataFrame({'count': frame})
                        else:
                            raise Exception(
                                f'No Data found between {datetime.strftime(date[0],"%d/%m/%Y")} and {datetime.strftime(date[1],"%d/%m/%Y")}')
                    elif place.title() in self.city:
                        city_filter = self.raw[self.raw['detectedcity'] == place.title(
                        )]
                        date_filter = city_filter[(city_filter['dateannounced'] >= date[0]) & (
                            city_filter['dateannounced'] <= date[1])]
                        if date_filter.empty == False:
                            frame = pd.concat(
                                [date_filter['dateannounced'], date_filter['gender']], axis=1)
                            # print(frame)
                            frame = frame.groupby(['dateannounced'])[
                                'gender'].value_counts()
                            return pd.DataFrame({'count': frame})
                        else:
                            raise Exception(
                                f'No Data found between {datetime.strftime(date[0],"%d/%m/%Y")} and {datetime.strftime(date[1],"%d/%m/%Y")}')
                else:
                    date = datetime.strptime(date, '%d/%m/%Y')
                    try:
                        state = self.code[place]

                    except:
                        if 'and' in place.split(' '):
                            words = []
                            for i in place.split(" "):
                                if i != 'and':
                                    words.append(i.title())
                                else:
                                    words.append(i)
                            state = ' '.join(words)
                        else:
                            state = place.title()
                    if state in self.state:
                        state_filter = self.raw[self.raw['detectedstate'] == state]
                        date_filter = state_filter[state_filter['dateannounced'] == date]
                        if date_filter.empty == False:

                            frame = pd.concat([date_filter['detecteddistrict'], date_filter['detectedcity'],
                                               date_filter['dateannounced'], date_filter['gender']], axis=1)
                            frame = frame.groupby(['detecteddistrict', 'detectedcity', 'dateannounced'])[
                                'gender'].value_counts()
                            return pd.DataFrame({'count': frame})
                        else:
                            print(
                                f'No Data found for {datetime.strftime(date,"%d/%m/%Y")}')
                    elif place.title() in self.district:
                        district_filter = self.raw[self.raw['detecteddistrict'] == place.title(
                        )]
                        date_filter = district_filter[district_filter['dateannounced'] == date]
                        if date_filter.empty == False:
                            frame = pd.concat(
                                [date_filter['detectedcity'], date_filter['dateannounced'], date_filter['gender']], axis=1)
                            # print(frame)
                            frame = frame.groupby(['detectedcity', 'dateannounced'])[
                                'gender'].value_counts()
                            return pd.DataFrame({'count': frame})
                        else:
                            raise Exception(
                                f'No Data found for {datetime.strftime(date,"%d/%m/%Y")}')
                    elif place.title() in self.city:
                        city_filter = self.raw[self.raw['detectedcity'] == place.title(
                        )]
                        date_filter = city_filter[city_filter['dateannounced'] == date]
                        if date_filter.empty == False:
                            frame = pd.concat(
                                [date_filter['dateannounced'], date_filter['gender']], axis=1)
                            # print(frame)
                            frame = frame.groupby(['dateannounced'])[
                                'gender'].value_counts()
                            return pd.DataFrame({'count': frame})
                        else:
                            raise Exception(
                                f'No Data found for {datetime.strftime(date,"%d/%m/%Y")}')
            else:
                try:
                    state = self.code[place]

                except:
                    if 'and' in place.split(' '):
                        words = []
                        for i in place.split(" "):
                            if i != 'and':
                                words.append(i.title())
                            else:
                                words.append(i)
                        state = ' '.join(words)
                    else:
                        state = place.title()
                if state in self.state:
                    state_filter = self.raw[self.raw['detectedstate'] == state]
                    if state_filter.empty == False:
                        frame = pd.concat([state_filter['detecteddistrict'], state_filter['detectedcity'],
                                           state_filter['dateannounced'], state_filter['gender']], axis=1)
                        frame = frame.groupby(['detecteddistrict', 'detectedcity', 'dateannounced'])[
                            'gender'].value_counts()
                        return pd.DataFrame({'count': frame})
                    else:
                        raise Exception(f'No Data found')
                elif place.title() in self.district:
                    district_filter = self.raw[self.raw['detecteddistrict'] == place.title(
                    )]
                    if district_filter.empty == False:
                        frame = pd.concat(
                            [district_filter['detectedcity'], district_filter['dateannounced'], district_filter['gender']], axis=1)
                        # print(frame)
                        frame = frame.groupby(['detectedcity', 'dateannounced'])[
                            'gender'].value_counts()
                        return pd.DataFrame({'count': frame})
                    else:
                        raise Exception(f'No Data found')
                elif place.title() in self.city:
                    city_filter = self.raw[self.raw['detectedcity']
                                           == place.title()]
                    if city_filter.empty == False:
                        frame = pd.concat(
                            [city_filter['dateannounced'], city_filter['gender']], axis=1)
                        # print(frame)
                        frame = frame.groupby(['dateannounced'])[
                            'gender'].value_counts()
                        return pd.DataFrame({'count': frame})
                    else:
                        raise Exception(f'No Data found')
        else:
            if date == 'all':
                frame = pd.concat(
                    [self.raw['detectedstate'], self.raw['dateannounced'], self.raw['gender']], axis=1)
                frame = frame.groupby(['detectedstate', 'dateannounced'])[
                    'gender'].value_counts()
                return pd.DataFrame({'count': frame})
            else:
                if '-' in date:
                    date = date.split('-')
                    date = [datetime.strptime(i, '%d/%m/%Y') for i in date]
                    date_filter = self.raw[(self.raw['dateannounced'] >= date[0]) & (
                        self.raw['dateannounced'] <= date[1])]
                    if date_filter.empty == False:
                        frame = pd.concat(
                            [date_filter['detectedstate'], date_filter['dateannounced'], date_filter['gender']], axis=1)
                        frame = frame.groupby(['detectedstate', 'dateannounced'])[
                            'gender'].value_counts()
                        return pd.DataFrame({'count': frame})
                    else:
                        raise Exception(
                            f'No Data found between {datetime.strftime(date[0],"%d/%m/%Y")} and {datetime.strftime(date[1],"%d/%m/%Y")}')
                else:
                    date = datetime.strptime(date, '%d/%m/%Y')
                    date_filter = self.raw[self.raw['dateannounced'] == date]
                    if date_filter.empty == False:
                        frame = pd.concat(
                            [date_filter['detectedstate'], date_filter['dateannounced'], date_filter['gender']], axis=1)
                        frame = frame.groupby(['detectedstate', 'dateannounced'])[
                            'gender'].value_counts()
                        return pd.DataFrame({'count': frame})
                    else:
                        raise Exception(
                            f'No Data found for {datetime.strftime(date,"%d/%m/%Y")}')


# Data class can apply various filters on collected datasets(Confirmed,Recovered,Deceased)
# based on User's choice
class Data(initializer):
    def __init__(self, init):
        self.csv_Confirmed = init.csv_Confirmed
        self.csv_recovered = init.csv_recovered
        self.csv_Death = init.csv_Death
        self.count_conf = init.count_conf
        self.count_recover = init.count_recover
        self.count_death = init.count_death
        self.code = init.code

    def __Dataset(self, date, confirmed, recovered, death):

        new = confirmed[['STATE/UT', date]]
        new = pd.concat([new, recovered[date], death[date]], axis=1)
        new.columns = ['State', 'Total Confirmed',
                       'Total Recovered', 'Total Death']
        return new

    def get_dataset_state(self, state='Whole', daily=False):
        '''
        this method of Data class will allow user to get cumulative counts of a particular 
        state.

        Parameters
        ----------
        state : character, optional
            name of state in India. The default is 'Whole'.
            state code is also applicable.If not given data for all states will be shown.
        daily : bool, optional
            If True Daily Count data will be shown. The default is False.

        Raises
        ------
        Exception
            If state/state code is wrong it will raise exception.

        Returns
        -------
        df : DataFrame
            if state is whole and daily is Flase then it Returns a dataframe consisting all states having 
            cumulative count of totalconfirmed,total recovered,total death till the previous day of the day of using this package.
            Otherwise for daily is True it will return dictionary of dataframes having confirmed,recovered and death cases for all states.
            if state is mentioned and daily is true then it will return a dataframe consisting all dates showing daily confirmed,daily recovered and
            daily death.

            if state is mentioned and daily is False then a dataframe will be returned consisting of name of districts of that states along with only 
            confirmed data.

        '''
        if state == 'Whole':
            if daily != True:
                df = pd.concat([self.csv_Confirmed[['STATE/UT', 'CODE', self.csv_Confirmed.columns[-1]]],
                                self.csv_recovered[self.csv_recovered.columns[-1]], self.csv_Death[self.csv_Death.columns[-1]]], axis=1)
                df.columns = ['STATE/UT', 'CODE', 'Total Confirmed',
                              'Total Recovered', 'Total Death']
                return df.drop(columns=['CODE'])
            else:
                return {'Confirmed': self.count_conf, 'Recovered': self.count_recover,
                        'Death': self.count_death}
        else:
            try:
                try:
                    state = self.code[state]

                except:
                    if 'and' in state.split(' '):
                        words = []
                        for i in state.split(" "):
                            if i != 'and':
                                words.append(i.title())
                            else:
                                words.append(i)
                        state = ' '.join(words)
                    else:
                        state = state.title()

                if daily != True:
                    flag = 0
                    json_url = urllib.request.urlopen(
                        'https://api.covid19india.org/v2/state_district_wise.json')
                    data = json.loads(json_url.read())
                    for i in data:
                        if i['state'] == state:
                            flag = 1
                            df = pd.DataFrame(i['districtData'])
                            col_dict = {i: j for j, i in enumerate(df.columns)}
                            df = df.iloc[:, [
                                col_dict['district'], col_dict['confirmed'], col_dict['recovered'], col_dict['deceased']]]
                            g = np.append(df.values, [['Total', df.iloc[:, 1:].sum()['confirmed'], df.iloc[:, 1:].sum()[
                                          'recovered'], df.iloc[:, 1:].sum()['deceased']]], axis=0)
                            # array=df.values.append(['Total',df.iloc[:,1:].sum()['confirmed'],df.iloc[:,1:].sum()['deceased'],df.iloc[:,1:].sum()['recovered']])
                            g = pd.DataFrame(g)
                            g.columns = df.columns
                            return g
                            break
                    if flag == 0:
                        print('No Confirmed Data in', state)
                else:
                    confirmed = self.count_conf[self.count_conf['STATE/UT']
                                                == state].iloc[:, 1:].T
                    recovered = self.count_recover[self.count_recover['STATE/UT']
                                                   == state].iloc[:, 1:].T
                    death = self.count_death[self.count_death['STATE/UT']
                                             == state].iloc[:, 1:].T
                    district_dict = {'Confirmed': confirmed[confirmed.columns[0]],
                                     'Recovered': recovered[recovered.columns[0]], 'Death': death[death.columns[0]]}
                    return pd.DataFrame(district_dict)
            except:
                raise Exception('No such states/state code')

    def get_dataset_by_date(self, date):
        '''
        This method of Data Class will allow user to get cumulative count of all states of
        total confirmed,total death and total recovered
        India for a particular given date

        Parameters
        ----------
        date : character
            Should be in dd/mm/yyyy format.

        Returns
        -------
        df : Dataframe
            Dataframe consisting all cumulative values of total confirmed,total recovered,total
            death for a given date.

        '''
        date = '{d.month}/{d.day}/{d.year}'.format(
            d=datetime.strptime(date, '%d/%m/%Y'))
        df = self.__Dataset(date, self.csv_Confirmed,
                            self.csv_recovered, self.csv_Death)
        return df

    def get_cum_dataset_between_date(self, startDate, endDate, by):
        '''
        This method of Data class will give cumulative counts between two given dates
        for all states 

        Parameters
        ----------
        startDate : character
            date format dd/mm/yyyy.
        endDate : character
            date format dd/mm/yyyy.
        by : character
            'Total Confirmed' or 'Total Recovered' or 'Total Death'.

        Raises
        ------
        Exception
            startdate should be less than endDate---if not it will raise exception.

        Returns
        -------
        df : Dataframe
            returns a dataframe of cumulative counts between two dates for all states by
            'Total Confirmed' or 'Total Recovered' or 'Total Death'.

        '''
        dateDict = {i: j for j, i in enumerate(self.csv_Confirmed.columns)}
        if datetime.strptime(startDate, '%d/%m/%Y') < datetime.strptime(endDate, '%d/%m/%Y'):
            start = '{d.month}/{d.day}/{d.year}'.format(
                d=datetime.strptime(startDate, '%d/%m/%Y'))
            end = '{d.month}/{d.day}/{d.year}'.format(
                d=datetime.strptime(endDate, '%d/%m/%Y'))
            if by.lower() == 'total confirmed':
                df = self.csv_Confirmed.iloc[:,
                                             dateDict[start]:dateDict[end]+1]
                df = pd.concat([self.csv_Confirmed['STATE/UT'], df], axis=1)
            elif by.lower() == 'total recovered':
                df = self.csv_recovered.iloc[:,
                                             dateDict[start]:dateDict[end]+1]
                df = pd.concat([self.csv_recovered['STATE/UT'], df], axis=1)
            elif by.lower() == 'total death':
                df = self.csv_Death.iloc[:, dateDict[start]:dateDict[end]+1]
                df = pd.concat([self.csv_Death['STATE/UT'], df], axis=1)
            return df
        else:
            raise Exception('Startdate must be less than EndDate')

    def get_count_between_date(self, startDate, endDate, by):
        '''
        Gives daily count data for all states between two dates

        Parameters
        ----------
        startDate : character
            date format dd/mm/yyyy
        endDate : character
            date format dd/mm/yyyy.
        by : character
            'Confirmed' or 'Recovered' or 'Death'.

        Raises
        ------
        Exception
            Startdate must be less than enddate.If not it raise anexception.
            it also raise error for wrong input in by parameter.

        Returns
        -------
        df : DataFrame
            DataFrame consisting daily counts for between two given dates
            for given by parameter.

        '''
        dateDict = {i: j for j, i in enumerate(self.count_conf.columns)}
        if datetime.strptime(startDate, '%d/%m/%Y') < datetime.strptime(endDate, '%d/%m/%Y'):
            start = '{d.month}/{d.day}/{d.year}'.format(
                d=datetime.strptime(startDate, '%d/%m/%Y'))
            end = '{d.month}/{d.day}/{d.year}'.format(
                d=datetime.strptime(endDate, '%d/%m/%Y'))

            try:
                if by.lower() == 'death':
                    df = self.count_death.iloc[:,
                                               dateDict[start]:dateDict[end]+1]
                    df = pd.concat([self.count_death['STATE/UT'], df], axis=1)
                elif by.lower() == 'recovered':
                    df = self.count_recover.iloc[:,
                                                 dateDict[start]:dateDict[end]+1]
                    df = pd.concat(
                        [self.count_recover['STATE/UT'], df], axis=1)
                elif by.lower() == 'confirmed':
                    df = self.count_conf.iloc[:,
                                              dateDict[start]:dateDict[end]+1]
                    df = pd.concat([self.count_conf['STATE/UT'], df], axis=1)
                return df
            except:
                raise Exception(
                    'by Argument must be "death" or "recovered" or "confirmed"')
        else:
            raise Exception('Startdate must be less than EndDate')

    def get_count_by_date(self, by, date=None):
        '''
        Gives the daily count of a given date or all dates by 'confirmed' or 'recovered'
        or 'death'

        Parameters
        ----------
        by : character
            'Confirmed' or 'Recovered' or 'Death'.
        date : character, optional
            if date(dd/mm/yyyy) is given count will be shown for that date. The default is None.

        Raises
        ------
        Exception
            If by argument is not within above mentioned and if year is not 2020 it will
            raise an exception.

        Returns
        -------
        df : dataframe
            dataframe consisting of counts of given date or all dates for all states .

        '''
        if date != None:
            if '{d.year}'.format(d=datetime.strptime(date, '%d/%m/%Y')) == '2020':
                date = '{d.month}/{d.day}/{d.year}'.format(
                    d=datetime.strptime(date, '%d/%m/%Y'))

                try:
                    if by.lower() == 'death':
                        df = self.count_death[date]
                        df = pd.concat(
                            [self.count_death['STATE/UT'], df], axis=1)
                    elif by.lower() == 'recovered':
                        df = self.count_recover[date]
                        df = pd.concat(
                            [self.count_recover['STATE/UT'], df], axis=1)
                    elif by.lower() == 'confirmed':
                        df = self.count_conf[date]
                        df = pd.concat(
                            [self.count_conf['STATE/UT'], df], axis=1)
                    return df
                except:
                    raise Exception(
                        'by Argument must be "death" or "recovered" or "confirmed"')
            else:
                raise Exception('Year must be 2020')
        else:
            try:
                if by.lower() == 'death':
                    df = self.count_death
                elif by.lower() == 'recovered':
                    df = self.count_recover
                elif by.lower() == 'confirmed':
                    df = self.count_conf
                return df
            except:
                raise Exception(
                    'by Argument must be "death" or "recovered" or "confirmed"')

    def rank(self, num, by, kind='top', cumulative=False, date=None):
        '''
        Gives top n or bottom n values as cumulative or daily basis for a date or
        combining whole dates filtered with by parameter.

        Parameters
        ----------
        num : integer
            number of rows user want to see.
            e.g num=10 -> top/bottom 10 data will be shown
        by : character
            'Total Confirmed' or 'Total Recovered' or 'Total Death'.
        kind : character, optional
            'top' or 'bottom' by which data will be filtered. The default is 'top'.
        cummulative : bool, optional
           if True it will show cumulative counts. The default is False.
        date : character, optional
            (must be in dd/mm/yyyy format)if date is given then method will return cumulative or daily count
            for that date. The default is None.
            if None it will return all cumulative/daily counts

        Raises
        ------
        Exception
            if date is None and cumulative is false then it is not possible to show
            data for top n or botom n rows..

        Returns
        -------
        dataframe/dictionary
            if date is not given and cummulative is False then it prompt to input state(state code or name)
            if state is set to 'all' it will return dictionary consisting all states having top/bottom counts
            otherwise a dataframe for a given state.
            whenever date is mentioned a dataframe will be returned consisting top/bottom cumulative count or 
            daily count for that date.

        '''
        if date != None:
            if cumulative == True:
                try:
                    df = self.get_dataset_by_date(date)
                    df = df.iloc[:-1,
                                 :].sort_values(by=by.title(), ascending=False)
                    if kind == 'top':
                        sort = df.head(num)
                    elif kind == 'bottom':
                        sort = df.tail(num)
                    return sort
                except:
                    raise Exception('Check date or by parameter')
            else:
                try:
                    df = self.get_count_by_date(by.split(' ')[1], date)
                    df = df.iloc[:-1,
                                 :].sort_values(by=df.columns[1], ascending=False)
                    if kind == 'top':
                        sort = df.head(num)
                    elif kind == 'bottom':
                        sort = df.tail(num)
                    return sort
                except:
                    raise Exception('Check date or by parameter')
        else:
            if cumulative == True:
                try:
                    df = self.get_dataset_state()
                    df = df.iloc[:-1,
                                 :].sort_values(by=by.title(), ascending=False)
                    if kind == 'top':
                        sort = df.head(num)
                    elif kind == 'bottom':
                        sort = df.tail(num)
                    return sort
                except:
                    raise Exception('Check date or by parameter')
            else:
                d = {}
                try:
                    count_data = self.get_count_by_date(by=by.split(' ')[1])
                    count_data = count_data.set_index('STATE/UT').T
                    for col in count_data.columns:
                        if kind == 'top':
                            d[col] = count_data[col].sort_values(
                                ascending=False)[:num]
                        else:
                            d[col] = count_data[col].sort_values(
                                ascending=False)[-num:]
                    del d['Total']
                    return d
                except:
                    raise Exception('Select right by parameter')

# defing visualizer class that contains the methods of plotting colleted data


class visualizer(initializer):
    def __init__(self, init):
        '''
        Gather all information to perform the visualization

        Parameters
        ----------
        init : TYPE
            None.

        Returns
        -------
        None.

        '''
        self.csv_Confirmed = init.csv_Confirmed
        self.csv_recovered = init.csv_recovered
        self.csv_Death = init.csv_Death
        self.count_conf = init.count_conf
        self.count_recover = init.count_recover
        self.count_death = init.count_death
        self.code = init.code
        column_dict = {i: j for j, i in enumerate(self.csv_Confirmed.columns)}
        count_dict = {i: j for j, i in enumerate(self.count_conf.columns)}
        self.date = pd.Series(
            self.csv_Confirmed.columns[column_dict['1/30/2020']:])
        self.confirmed = pd.Series(
            self.csv_Confirmed[self.csv_Confirmed['STATE/UT'] == 'Total'].iloc[:, column_dict['1/30/2020']:].values[0])
        self.recovered = pd.Series(
            self.csv_recovered[self.csv_recovered['STATE/UT'] == 'Total'].iloc[:, column_dict['1/30/2020']:].values[0])
        self.death = pd.Series(
            self.csv_Death[self.csv_Death['STATE/UT'] == 'Total'].iloc[:, column_dict['1/30/2020']:].values[0])
        self.count_confirmed = pd.Series(
            self.count_conf[self.count_conf['STATE/UT'] == 'Total'].iloc[:, count_dict['1/30/2020']:].values[0])
        self.count_recovered = pd.Series(
            self.count_recover[self.count_recover['STATE/UT'] == 'Total'].iloc[:, count_dict['1/30/2020']:].values[0])
        self.count_Death = pd.Series(
            self.count_death[self.count_death['STATE/UT'] == 'Total'].iloc[:, count_dict['1/30/2020']:].values[0])

    def __graph(self, x, confirmed, recovered, death, title=None, date=True):
        '''
        A private method used by visualizer class methods to generate 3 subplots graphs

        Parameters
        ----------
        x : series-like

        confirmed : series-like

        recovered : series-like

        death : series-like

        date : bool, optional
             The default is True.

        Returns
        -------
        Generate 3 subplots.

        '''
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=False)
        fig.set_size_inches(23.5, 15.5)
        c_max = max(confirmed)
        r_max = max(recovered)
        d_max = max(death)
        df_max = max([c_max, r_max, d_max])
        # print(date)
        if date != True:
            x_min = min(x)
            x_max = max(x)
            ax1.scatter(x, confirmed, marker='o', color='red', s=[
                        i for i in confirmed], edgecolors='black')
            ax1.set_ylabel('Confirmed cases', labelpad=20)
            ax1.yaxis.set_ticks(np.arange(0, df_max, df_max/10))
            ax1.xaxis.set_ticks(np.arange(x_min, x_max, (x_max-x_min)/10))
            ax2.scatter(x, recovered, marker='o', color='green', s=[
                        i for i in recovered], edgecolors='black')
            ax2.yaxis.set_ticks(np.arange(0, df_max, df_max/10.))
            ax2.xaxis.set_ticks(np.arange(x_min, x_max, (x_max-x_min)/10))
            ax2.set_ylabel('Total recovered', labelpad=20)
            ax3.scatter(x, death, marker='o', color='blue', s=[
                        i for i in death], edgecolors='black')
            ax3.yaxis.set_ticks(np.arange(0, df_max, df_max/10))
            ax3.set_ylabel('Total deceased', labelpad=20)
            ax3.xaxis.set_ticks(np.arange(x_min, x_max, (x_max-x_min)/10))
            ax3.set_xlabel('Latitude', labelpad=20)
            if title != None:
                fig.suptitle(title, fontsize=30)
        else:
            ax1.plot(x, confirmed, marker='*', color='red')
            ax1.set_ylabel('Confirmed cases', labelpad=20)
            if df_max != 0:
                ax1.yaxis.set_ticks(np.arange(0, df_max, df_max/10))
            #ax1.tick_params(axis ='x', rotation = 45)
            ax2.plot(x, recovered, marker='*', color='green')

            ax2.set_ylabel('Total recovered', labelpad=20)
            #ax2.tick_params(axis ='x', rotation = 45)
            ax3.plot(x, death, marker='*', color='blue')
            if df_max != 0:
                ax2.yaxis.set_ticks(np.arange(0, df_max, df_max/10))
                ax3.yaxis.set_ticks(np.arange(0, df_max, df_max/10))
            ax3.set_ylabel('Total deceased', labelpad=20)
        # ax[1][0].set_ybound(0,1500)
            '''ax[1][0].set_title('Recovered cases')
            ax[2][0].plot(dateseries_dead)
            ax[2][0].set_title('Dead cases')'''
            fig.autofmt_xdate()
            ax3.tick_params(axis='x', rotation=45)
            if title != None:
                fig.suptitle(title, fontsize=25)

        plt.show()

    def whole(self, title=None, daily=False):
        '''
        Generate 3 subplots of whole collected data 

        Parameters
        ----------
        title : Character, optional
            Sets the title of the subplots. The default is None.
        daily : bool, optional
            if True garph will be plotted on daily counts otherwise on cumulative counts. The default is False.

        Returns
        -------
        3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased.
        may be daily or cumulative based on daily parameter passed.

        '''
        if daily == True:
            self.__graph(self.date, self.count_confirmed,
                         self.count_recovered, self.count_Death, title=title)
        else:
            self.__graph(self.date, self.confirmed,
                         self.recovered, self.death, title=title)

    def tail(self, num, title=None, daily=False):
        '''
        Gives graphical visualization of latest n(=num) dayes based on daily or cumulative data

        Parameters
        ----------
        title : Character, optional
            Sets the title of the subplots. The default is None.
        num : integer
            setd the number of latest dates user wants to see.
        daily : bool, optional
            if true graph is plotted based on daily data. The default is False.

        Returns
        -------
        3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased.
        may be daily or cumulative based on daily parameter passed.
        '''
        if daily != False:
            date = self.date[len(self.date)-num:]
            confirmed = self.count_confirmed[len(self.count_confirmed)-num:]
            recovered = self.count_recovered[len(self.count_recovered)-num:]
            death = self.count_Death[len(self.count_Death)-num:]
            if title != None:
                self.__graph(date, confirmed, recovered, death, title=title)
            else:
                self.__graph(date, confirmed, recovered, death)
        else:
            date = self.date[len(self.date)-num:]
            confirmed = self.confirmed[len(self.confirmed)-num:]
            recovered = self.recovered[len(self.recovered)-num:]
            death = self.death[len(self.death)-num:]
            if title != None:
                self.__graph(date, confirmed, recovered, death, title=title)
            else:
                self.__graph(date, confirmed, recovered, death)

    def head(self, num, title=None, daily=False):
        '''
        Gives graphical visualization of first n(=num) dayes based on daily or cumulative data

        Parameters
        ----------
        title : Character, optional
            Sets the title of the subplots. The default is None.
        num : integer
            setd the number of dates from start user wants to see.
        daily : bool, optional
            if true graph is plotted based on daily data. The default is False.

        Returns
        -------
        3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased.
        may be daily or cumulative based on daily parameter passed.

        '''
        if daily != False:
            date = self.date[:num]
            confirmed = self.count_confirmed[:num]
            recovered = self.count_recovered[:num]
            death = self.count_Death[:num]
            if title != None:
                self.__graph(date, confirmed, recovered, death, title=title)
            else:
                self.__graph(date, confirmed, recovered, death)
        else:
            date = self.date[:num]
            confirmed = self.confirmed[:num]
            recovered = self.recovered[:num]
            death = self.death[:num]
            if title != None:
                self.__graph(date, confirmed, recovered, death, title=title)
            else:
                self.__graph(date, confirmed, recovered, death, title=title)

    def graph_by_date(self, startDate, endDate, state=None, title=None, daily=False):
        '''
        Gives the visualization of cumulative data or daily data between two given
        dates for a given state or as whole india.

        Parameters
        ----------
        title : Character, optional
            Sets the title of the subplots. The default is None.
        startDate : character
            dd/mm/yyyy format(e.g 02/04/2020).
        endDate : character
            dd/mm/yyyy format(e.g 02/04/2020).
        state : character, optional
            for which state graph will be plotted.If None graph will be plotted for whole india. The default is None.
            states input also takes state codes.
        daily : bool, optional
            if True graph will plotted daily basis. The default is False.

        Raises
        ------
        Exception
            startdate must be less than enddate and if states are given wrong it will raise exception.

        Returns
        -------
        3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased for a state or whole india
        between two dates.
        may be daily or cumulative based on daily parameter passed.

        '''
        column_dict = {i: j for j, i in enumerate(self.csv_Confirmed.columns)}
        count_dict = {i: j for j, i in enumerate(self.count_conf.columns)}
        if datetime.strptime(startDate, '%d/%m/%Y') < datetime.strptime(endDate, '%d/%m/%Y'):
            start = '{d.month}/{d.day}/{d.year}'.format(
                d=datetime.strptime(startDate, '%d/%m/%Y'))
            end = '{d.month}/{d.day}/{d.year}'.format(
                d=datetime.strptime(endDate, '%d/%m/%Y'))

            if state != None:
                try:
                    try:
                        state = self.code[state]
                    except:
                        if 'and' in state.split(' '):
                            words = []
                            for i in state.split(" "):
                                if i != 'and':
                                    words.append(i.title())
                                else:
                                    words.append(i)
                            state = ' '.join(words)
                        else:
                            state = state.title()
                    if daily == False:

                        date = self.date[self.date[self.date == start].index[0]
                            :self.date[self.date == end].index[0]+1]
                        confirmed = pd.Series(
                            self.csv_Confirmed[self.csv_Confirmed['STATE/UT'] == state].iloc[:, column_dict[start]:column_dict[end]+1].values[0])
                        recovered = pd.Series(
                            self.csv_recovered[self.csv_Confirmed['STATE/UT'] == state].iloc[:, column_dict[start]:column_dict[end]+1].values[0])
                        death = pd.Series(
                            self.csv_Death[self.csv_Death['STATE/UT'] == state].iloc[:, column_dict[start]:column_dict[end]+1].values[0])
                        if title != None:
                            self.__graph(date, confirmed,
                                         recovered, death, title=title)
                        else:
                            self.__graph(date, confirmed, recovered, death)
                    else:

                        date = self.date[self.date[self.date == start].index[0]
                            :self.date[self.date == end].index[0]+1]
                        confirmed = pd.Series(
                            self.count_conf[self.count_conf['STATE/UT'] == state].iloc[:, count_dict[start]:count_dict[end]+1].values[0])
                        recovered = pd.Series(
                            self.count_recover[self.count_recover['STATE/UT'] == state].iloc[:, count_dict[start]:count_dict[end]+1].values[0])
                        death = pd.Series(
                            self.count_death[self.count_death['STATE/UT'] == state].iloc[:, count_dict[start]:count_dict[end]+1].values[0])
                        if title != None:
                            self.__graph(date, confirmed,
                                         recovered, death, title=title)
                        else:
                            self.__graph(date, confirmed, recovered, death)
                except:
                    raise Exception('No such state or state code')
            else:
                if daily == False:

                    date = self.date[self.date[self.date == start].index[0]:self.date[self.date == end].index[0]+1]
                    confirmed = self.confirmed[self.date[self.date ==
                                                         start].index[0]:self.date[self.date == end].index[0]+1]
                    recovered = self.recovered[self.date[self.date ==
                                                         start].index[0]:self.date[self.date == end].index[0]+1]
                    death = self.death[self.date[self.date == start].index[0]:self.date[self.date == end].index[0]+1]
                    self.__graph(date, confirmed, recovered, death)
                else:

                    date = self.date[self.date[self.date == start].index[0]:self.date[self.date == end].index[0]+1]
                    confirmed = self.count_confirmed[self.date[self.date ==
                                                               start].index[0]:self.date[self.date == end].index[0]+1]
                    recovered = self.count_recovered[self.date[self.date ==
                                                               start].index[0]:self.date[self.date == end].index[0]+1]
                    death = self.count_Death[self.date[self.date ==
                                                       start].index[0]:self.date[self.date == end].index[0]+1]
                    if title != None:
                        self.__graph(date, confirmed, recovered,
                                     death, title=title)
                    else:
                        self.__graph(date, confirmed, recovered, death)
        else:
            raise Exception('Startdate should be less than Enddate')

    def plot_by_latitude(self, title=None):
        '''
        Gives the visualization of counts with respect to state latitudes

        Parameters
        ----------
        title : Character, optional
            Sets the title of the subplots. The default is None.

        Returns
        -------
        3 subplots consisting latitude vs latitude confirmed,latitudes vs total recovered,latitudes vs total deceased.

        '''

        newConf = self.csv_Confirmed.sort_values(by=['LATITUDE'])
        newRec = self.csv_recovered.sort_values(by=['LATITUDE'])
        newDeath = self.csv_Death.sort_values(by=['LATITUDE'])
        latitude = newConf['LATITUDE'][:-1]
        confirmed = newConf[newConf.columns[-1]][:-1]
        recovered = newRec[newRec.columns[-1]][:-1]
        death = newDeath[newDeath.columns[-1]][:-1]
        if title != None:
            self.__graph(latitude, confirmed, recovered,
                         death, date=False, title=title)
        else:
            self.__graph(latitude, confirmed, recovered, death, date=False)
