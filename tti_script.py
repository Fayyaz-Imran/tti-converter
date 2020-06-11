import pandas as pd
import numpy as np

#Initiate dataset setup

#import source csv
df = pd.read_csv('tti_stats.csv')
df.columns = ['day', 'hr', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']

#fills missing days column forwardly
df['fix_day'] = df['day'].fillna(method='ffill')

#create new df with fixed values
new_df = df[['fix_day', 'hr', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']].copy()

#get last row value for generating new table
total_days = new_df['fix_day'].iat[-1]


#Initiate dataset setup
def convert():
    #Count variable
    count_day = 1
    df_final = pd.DataFrame(columns=['fix_day', 'hr', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

    while count_day < total_days+1:
        #filter by days
        day = new_df['fix_day'] == count_day
        day_df = new_df[day]
        df1 = day_df
        print("Processing data for day" +str(count_day))

        #create expected table 
        exp_df = pd.read_csv('fix_hour.csv')
        df2 = exp_df

        #Dataframe combine 
        df3 = df2.merge(df1,on='hr',how="left")
        df3['fix_day_x'] = df3['fix_day_x'].fillna(df3['fix_day_y'])
        df3.drop(["fix_day_y"], inplace=True, axis=1)
        df3.rename(columns={'fix_day_x':'fix_day'}, inplace=True)
        df3['fix_day'] = df3['fix_day'].bfill()
        df3['fix_day'] = df3['fix_day'].fillna(method='ffill')
        df_final = df_final.append(df3)
        count_day += 1
    else:
        df_final.to_csv("tti_final.csv", index=False, encoding='utf-8-sig')
        print("Dataset processed!")
        

#Run Script
def main():
    convert()


if __name__ == "__main__":
    main()