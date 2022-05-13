# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:02:31 2022

@author: au685355 Ida Anthonj Nissen
"""

# %% Import google fact check data
import ndjson
import pandas as pd

path = 'DIRECTORY_HERE'
language_code = 'pl'    #'de'    #it, pl
#query = ['ukrain', 'selenskyj', 'russland', 'putin', 'kiew']    #german
#query = ['ukrain', 'ucrain', 'zelensky', 'russia', 'putin', 'kiev']    #italian
query = ['ukrain', 'zełenski', 'rosja', 'putin', 'Kijów']    #polish

#Put all result files into one list
data_extr_all = []
for i in range(len(query)):
    json_file = path + '\\' + query[i] + '-' + language_code + '.ndjson'
    print(json_file)
     
    with open(json_file, encoding="utf8") as f:
        data_extr = ndjson.load(f)
        print(len(data_extr))
        data_extr_all.extend(data_extr)
    
    
# Take out duplicates
seen = set()
data_extr_nodup = []
#for item in data_extr['text']:
for i in range(len(data_extr_all)):
    if data_extr_all[i]['text'] not in seen:
        seen.add(data_extr_all[i]['text'])
        data_extr_nodup.append(data_extr_all[i])

data_extr_all = data_extr_nodup
del data_extr_nodup


# Take out stories from Dec 21 to Mar 22
data_DecMar = []
#Use review date as this it the date the local fact-checkers websites have used
for i in range(len(data_extr_all)):
    if 'reviewDate' in data_extr_all[i]['claimReview'][0]:
        tmp = data_extr_all[i]['claimReview'][0]['reviewDate']
        if tmp[0:7] == '2021-12' or tmp[0:7] == '2022-01' or tmp[0:7] == '2022-02' or tmp[0:7] == '2022-03': 
            data_DecMar.append(data_extr_all[i])

#Check if language code is correct and take those out with wrong language code
data_lang = []
for i in range(len(data_DecMar)):
    if data_DecMar[i]['claimReview'][0]['languageCode'] == language_code:
        data_lang.append(data_DecMar[i])


#%% Extract claim title, url, date and fact-checker

# put claim titles into list
list_claim = [ sub['text'] for sub in data_DecMar ]

#put review date into list
list_date = [ sub['claimReview'][0]['reviewDate'] for sub in data_DecMar ]

# Extract publisher / debunker
list_pub = []
for i in range(len(data_DecMar)):
    if 'name' in data_DecMar[i]['claimReview'][0]['publisher']:
        list_pub.append(data_DecMar[i]['claimReview'][0]['publisher']['name'])
    elif 'site' in data_DecMar[i]['claimReview'][0]['publisher']:
        list_pub.append(data_DecMar[i]['claimReview'][0]['publisher']['site'])

#Extract url
list_url =  [ sub['claimReview'][0]['url'] for sub in data_DecMar ]


#%% Combine into one dataframe
dict = {'date': list_date, 'title': list_claim, 'publisher': list_pub, 'url': list_url}   
df = pd.DataFrame(dict)
df.sort_values(by=['date'], inplace=True, ascending=False, ignore_index=True)


#%%
#Import excel file with scraped stories from the local websites
#data_local = pd.read_excel('FILENAME_HERE.xlsx') #Load Your Dataframe
#data_local = pd.read_excel('FILENAME_HERE.xlsx') #Load Your Dataframe
data_local = pd.read_excel('FILENAME_HERE.xlsx') #Load Your Dataframe
data_local.head()

#Compare the two lists with urls: check if the Google API urls are not already in the local excel list
#occurrence = df.merge(data_local, left_on='url' , right_on='url1', how='left', indicator=True)
occurrence = df.merge(data_local, left_on='url' , right_on='url', how='left', indicator=True)
occurrence.drop_duplicates(subset=['title_x'], keep='first', inplace=True, ignore_index=True)   #the polish comparison yielded two dublicates, at index 3 and 121
left_only = occurrence[occurrence["_merge"] == "left_only"]
#use the index to filter the Google API stories dataframe
df_filtered = df.iloc[left_only.index, :]


#%% Export to excel
file_name = language_code + '_Google_API_extra'
df_filtered.to_csv(r'DIRECTORY_HERE\{}.csv'.format(file_name), index=False, encoding='utf-8-sig')
