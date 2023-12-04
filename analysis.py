import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def perform_analysis(patientID, activity_path, sleep_path):
    patientID = int(patientID)
    def remove_date(text):
        return text.split(' ')[0]

   # activity_path = '/Users/keyanakomilian/Downloads/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv'
    #sleep_path = '/Users/keyanakomilian/Downloads/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv'
    daily_activity = pd.read_csv(activity_path)
    daily_sleep = pd.read_csv(sleep_path)

    daily_activity.rename(columns={'ActivityDate': 'Date'}, inplace=True)
    daily_sleep.rename(columns={'SleepDay': 'Date'}, inplace=True)

    daily_sleep['Date'] = daily_sleep['Date'].apply(remove_date)
    daily_info = pd.merge(daily_activity, daily_sleep, on = ['Id', 'Date'])

    daily_info['percent active'] = ( (daily_info['VeryActiveMinutes'] + daily_info['FairlyActiveMinutes'] ) / (daily_info['LightlyActiveMinutes'] + daily_info['FairlyActiveMinutes'] + daily_info['VeryActiveMinutes'])) * 100
    daily_info['Risk'] = (1 - (daily_info['TotalMinutesAsleep'] / 420)) * (1 - (daily_info['percent active'] / 100))

    data_patient = daily_info[daily_info['Id'] == patientID]
    #plt = sns.barplot(data=data_patient, x='Date', y='Risk')
    avg_risk = np.average(data_patient['Risk'])
    #plt.savefig('plot.png')
    return avg_risk, data_patient

#PATIENT IDS:
'''
['user_2320127002.csv', 
 'user_4702921684.csv', 
 'user_4319703577.csv', 
 'user_4445114986.csv', 
 'user_1644430081.csv', 
 'user_5577150313.csv',
'user_4388161847.csv', 
'user_2026352035.csv', 
'user_5553957443.csv', 
'user_1503960366.csv', 
'user_1844505072.csv', 
'user_2347167796.csv', 
'user_7086361926.csv', 
'user_3977333714.csv', 
'user_6117666160.csv', 
'user_4558609924.csv', 
'user_4020332650.csv', 
'user_8792009665.csv', 
'user_1927972279.csv', 
'user_8378563200.csv', 
'user_6962181067.csv', 
'user_6775888955.csv', 
'user_8053475328.csv', 
'user_7007744171.csv']
'''


#NAMES
'''
['Consuelo468_Nikolaus26',
'Cassondra930_Nicolas769', 
'Dorinda15_Robel940',
'Frederick289_Homenick806',
'Minerva230_Glover433', 
'Oliva247_Waters156',
'Cleopatra935_Stracke611',
'Hyman89_Kohler843', 
'Royce974_Abernathy524',
'Billie243_Halvorson124', 
'Josephine273_Kuvalis369',
'Caron739_Herzog843', 
'Lloyd546_Schaden604',
'Carmelina668_Keebler762', 
'Dominick530_Collier206',
'Karolyn830_Spinka232',
'Aletha771_Haley279',
'Santiago500_Navarrete760', 
'Emmett200_Doyle959',
'Jefferey580_Conroy74',
'Lane844_Hegmann834',
'Rex53_Kemmer137', 
'Eric487_Kulas532', 
'Marline710_Tromp100', 
'Lynn917_Hessel84',
'Georgann131_Fay398', 
'Whitley172_Bashirian201',
'Lorna458_Bashirian201', 
'Frances376_Sporer811', 
'Tessie155_Haag279', 
'Marietta439_Parisian75', 
'Miguel815_Tejeda887', 
'Jonah176_Lueilwitz711', 
'Rosette746_Dooley940', 
'Kendrick479_Spencer878', 
'Felipe97_Predovic534',
'Adell482_Parisian75']
'''
