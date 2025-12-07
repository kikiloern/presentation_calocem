#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
def read_calo(csv_file): 
    df = pd.read_csv(csv_file, 
    sep = ',', 
    decimal = '.', 
    skiprows = 16, 
    )    #read csv
    df = df.iloc[:,[0,-6,-5,-4,-3,-2,-1]] #select columns in a compatible fashion for old and new
    df = df.rename(columns={df.columns[0]: 'time',
                            df.columns[1]: "temperature",
                            df.columns[2]: "heat_flow", 
                            df.columns[3]: "heat", 
                            df.columns[4]: "heat_flow_normed", 
                            df.columns[5]: "heat_normed", 
                            df.columns[6]: 'time_marker'})  #rename columns
    df['time_marker']=df['time_marker'].ffill()    #fill time_marker NaN with buzz words
    df = df.dropna(subset=['time_marker'])     #drop NAN in time marker
    df = df[df['time_marker'] == "Reaction start. Measuring position. Signal correct"]      #only correct Signal
    df=df.reset_index(drop=True)    #reset index
    #df["time"]=df["time"]-df["time"][0]     #correct time
    del df["time_marker"]   #remove timer marker column
    df = df[df['time'] > 0] #only time > 0
    return df

#%%
JAA122 = read_calo(r'C:\Users\aleks\Desktop\presentation_calocem\data\JAA_CAL122.csv')
#JAA001 = read_calo(r'C:\Users\aleks\Desktop\presentation_calocem\data\JAA_CAL001.csv')

# %%
JAA122['heat_flow_normed']=JAA122['heat_flow']/4.00*1000
JAA122['heat_flow_normed']=JAA122['heat_flow']/4.00*1000
#JAA001['heat_flow_normed']=JAA001['heat_flow']/4.00*1000   #5,3333 + 2,66666 = 8g und wz = 0.5

#%%
fig = plt.figure(figsize=(4,3))#in inch, für cm '/2.54'

plt.plot(JAA122['time']/60/60, JAA122['heat_flow_normed'], label = 'CEM I 42.5R')
#plt.plot(JAA001['time']/60/60, JAA001['heat_flow_normed'], label = 'CEM I 42.5R')


plt.xlim(0,72)#von 0 bis 10 h
plt.ylim(0,3)
plt.xlabel('Time / h')
plt.ylabel('Normalized heat flow  / mW/g')
plt.legend(frameon = False, loc = 0)
plt.tight_layout(pad=0.33)
#plt.savefig('H:/TUM-PC/Desktop/Abbildungen Kalorimeter/KarlstadtKCitrat.png', dpi=300)
#plt.savefig('H:/TUM-PC/Desktop/Abbildungen Kalorimeter/KarlstadtKCitrat.svg')
#plt.savefig('H:/TUM-PC/Desktop/Abbildungen Kalorimeter/KarlstadtKCitrat.pdf')
#plt.savefig('H:/TUM-PC/Desktop/1.jpg')
# %%
