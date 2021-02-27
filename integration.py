#!/usr/local/bin/
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation, InRangeValidation, IsDistinctValidation 
import os

counties = ['Loudoun County','Washington County','Harlan County','Malheur County']
states = ['Virginia','Oregon','Kentucky','Oregon']
county_and_state = []
for i in range(0, 4):
    county_and_state.append(counties[i] + ' ' + states[i])

def display_df(df):
    with pd.option_context('display.max_rows', 123,'display.max_columns', None):
        print(df)

def agg_counties(csv):
    df = pd.read_csv(csv)
    #print(df.head())
    df = df.loc[:,['County','State','TotalPop','Poverty','IncomePerCap']]
    df['county_and_state'] = df['County'] + ' ' + df['State']
    df = df[df['county_and_state'].isin(county_and_state)]
    
    dfs = []
    totals = dict()
    i = 0
    for cs in county_and_state:
        dfs.append(df[df['county_and_state'] == cs])
        #print(dfs[i].head())
        #print(dfs[i].agg({'TotalPop':['sum']}))
        #totals.append( dfs[i].agg({'TotalPop' : ['sum']}) )
        #totals[cs] = ( dfs[i].agg({'TotalPop' : ['sum']}) )
        i += 1

    #print(totals)
    data = {'cs' : county_and_state, 'pop' : [0,0,0,0], 'pov' : [0,0,0,0], 'inc' : [0,0,0,0]}
    tot = pd.DataFrame(data)
    print(tot.head())
    i = 0
    for df in dfs:
        pop = 0
        for row in df:
            #print(df['TotalPop'])
            pop += df['TotalPop']
        print(pop)
        #tot.at[i,'pop'] = pop
        tot.loc[i,['pop']] = pop
        i += 1
    print(tot)
    

def main():
    agg_counties("acs2017_census_tract_data.csv")


if __name__ == "__main__":
    main()

'''
cen 2 County # County - name of the county
cen 1 State # State - name of the state in which the county resides
cov TotalCases - total number of COVID cases for this county as of February 20, 2021
cov Dec2020Cases - number of COVID cases recorded in this county in December of 2020
cov TotalDeaths - total number of COVID deaths for this county as of February 20, 2021
cov Dec2020Deaths - number of COVID deaths recorded in this county in December of 2020
cen 3 TotalPop # Population - population of this county
cen 17 Poverty # Poverty - % of people in poverty in this county
cen 15 IncomePerCap # PerCapitaIncome - per capita personal income for this county

counties:
    Loudon County Virginia, 
    Washington County Oregon, 
    Harlan County Kentucky, 
    Malheur County Oregon

need four data points per county: 
    total cases 
    total deaths 
    cases reported during December 2020
    deaths reported during December 2020

COVID CSV fields:
    date 
    county
    state
    fips
    cases
    deaths

census CSV:
    a lot

'''
