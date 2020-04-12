# CovidIndia Module

**Description**

This package has the power to bring all data of India as tabular form up to the latest data that is available from [the COVID-19 Indian Dataset maintained by University of Kalyani](https://github.com/kalyaniuniversity/COVID-19-Datasets). It will bring the whole raw, date wise timeseries data. It can also visualize the data of your choice of range of dates.You can also see the total confirmed, death and recovered by filtered the data set giving the date or range of dates. It can show the total confirmed cases with count of male and female with state, district and even
city filter. It can also produce output by date or range of date.

# How it works?

It gathers information from our own maintained database. Database data are collected from various websites, news channels and [covid19india.org crowdsourcing initiative](https://www.covid19india.org). From the collected data this module will help user to represent in user friendly format with all types of filters in one place. No need to search any website. Just use this module for India based Covid-19 projects.

## Installation

As of now, the code is kept open-source directly accessible from this repository. We are working on bringing it ot PyPI. Shall update the README as soon as we are done with it.

## Basic Usage

> from Covid.CovidIndia import \*
> #Initialize the module to collect the data
> Init=initializer()
> #shows the collected data in Dataframe formate
> Init.show_data()
> #sample output
> |STATE/UT | Total Confirmed|
> |------------- |------------------- |
> |West Bengal| 126 |
> |Maharashtra| 1761 |
> |Odisha | 54

## Examples

Examples are in github repository project folder.
