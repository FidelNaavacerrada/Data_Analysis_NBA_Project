import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')

'''We create dataframes from both excel gamelog files'''
LD = pd.read_excel(r'LUKA_ROOKIE_GAMELOGS.xlsx')
LBJ = pd.read_excel(r'LEBRON_ROOKIE_STATS.xlsx')

'''We analyse and clean both files, starting with the Luka file'''
#LD.info()

'''We look for invalid data to convert to NaN'''
#print(LD['PTS'].unique())

'''There is a game where the FT% should be 0 but is NaN instead,
so we change it to 0 so we can distinguish it afterwards'''
LD['FT%'] = LD['FT%'].replace(np.nan, 0)

LD = LD.replace(['Inactive'],np.nan)
LD = LD.replace(['Did Not Dress'],np.nan)

#print(LD.head(40))

'''We change null values to "Home" in "Home/Away" column'''
LD['Home/Away'] = LD['Home/Away'].replace([np.nan], 'Home')

'''Keep only year age from a year-day age format so we can store as an int, separating them in columns and deleting the
day column'''
parts = LD['Age'].str.split('-', expand=True)
LD['Age'] = parts[0]
LD['Age'] = LD['Age'].astype('int')

#print(LD.head())
#print(LD['Column2'])

parts = LD['Column2'].str.split(' ', expand=True)
LD['Column2'] = parts[0]
LD.rename(columns = {'Column2':'Win/Lose'}, inplace = True)

LD.drop('MP', inplace=True, axis=1)

'''Once our first dataframe is clean, we clean the next one'''

#LB.info()

LBJ['FT%'] = LBJ['FT%'].replace(np.nan, 0)
LBJ['3P%'] = LBJ['3P%'].replace(np.nan, 0)

LBJ = LBJ.replace(['Inactive'], np.nan)

LBJ.rename(columns = {'Column2': 'Win/Lose'}, inplace = True)
LBJ.rename(columns = {'Column1': 'Home/Away'}, inplace = True)

LBJ['Home/Away'] = LD['Home/Away'].replace([np.nan], 'Home')

parts = LBJ['Age'].str.split('-', expand=True)
LBJ['Age'] = parts[0]
LBJ['Age'] = LD['Age'].astype('int')

parts = LBJ['Win/Lose'].str.split(' ', expand=True)
LBJ['Win/Lose'] = parts[0]

LBJ.drop('MP', inplace=True, axis=1)

#LBJ.info()

'''We start comparing both player rookie seasons'''

'''Total games played for the season'''
ld_gp = 72
lbj_gp = 79

'''Function that will join selected columns from 2 dataframes and create a new one'''


def join2columns_ld_lbj(new_df1, new_df2):
    new_df = pd.concat([new_df1, new_df2], axis=0, ignore_index=False)
    new_df['Player'] = (len(new_df1) * (0,) + len(new_df2) * (1,))
    new_df.reset_index(inplace=True)
    new_df['Player'] = new_df['Player'].map({0: 'Luka', 1: 'LeBron'})
    return new_df


'''New dataframe creation which stores both top 10 scoring performances and its barplot'''
ld_mostpoints = LD['PTS'].nlargest(n=10).reset_index()
lbj_mostpoints = LBJ['PTS'].nlargest(n=10).reset_index()
pts10=join2columns_ld_lbj(ld_mostpoints, lbj_mostpoints)
#print(pts10)

sns.barplot(x='index', y='PTS', hue = 'Player', palette='hls', data=pts10).set(xlabel ="Game nº")
plt.show()

'''New data: percentage of type of shots for each player'''
'''Volume of 3P, 2P and FT shots for each one'''


def percentage_of(stat, df):
    new_perc = (df[stat].sum()*100)/(df['FGA'].sum()+df['FTA'].sum())
    return new_perc


ld3P = percentage_of('3PA', LD)
lbj3P = percentage_of('3PA', LBJ)
ldft = percentage_of('FTA', LD)
lbjft = percentage_of('FTA', LBJ)
ld2p = 100-(ld3P+ldft)
lbj2p = 100-(lbjft+lbj3P)

'''We create a dataframe and a plot using the shot percentages'''
#data = {'Shot Type': ['3P','3P', '2P','2P', 'FT', 'FT'], 'Data': [lbj3P,ld3P,  lbj2p,ld2p, lbjft, ldft], 'Player': ['LeBron','Luka', 'LeBron','Luka', 'LeBron', 'Luka']}
ld_pctg = pd.DataFrame({'Shot Type': ['3P', '2P', 'FT'], 'Data': [ld3P, ld2p, ldft]})
lbj_pctg = pd.DataFrame({'Shot Type': ['3P', '2P', 'FT'], 'Data': [lbj3P, lbj2p, lbjft]})
pctg_comp = join2columns_ld_lbj(ld_pctg, lbj_pctg)

sns.barplot(data=pctg_comp,x='Shot Type',y='Data', hue='Player').set(ylabel ="%")
plt.show()

'''We create a new dataframe that will help us visualize better the 3 point shot difference between both'''
ld3pa = LD['3PA'].reset_index()
lbj3pa = LBJ['3PA'].reset_index()
df3pa = join2columns_ld_lbj(ld3pa, lbj3pa)
print(df3pa)
sns.scatterplot(data=df3pa, x='index', y='3PA', hue = 'Player', palette='hls').set(xlabel='Game nº')
plt.show()